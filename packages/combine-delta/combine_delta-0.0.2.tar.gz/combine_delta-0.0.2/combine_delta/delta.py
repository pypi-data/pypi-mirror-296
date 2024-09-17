#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  26 10:06:00 2023

@author: mhamon

"""

import os
import glob
import time
import numpy as np
import xarray as xr


def init_ds(nt, dict_vars, dim_delta):
    """
    Initializes the default delta dataset (all variables are set to 0).
    """

    ds = xr.Dataset()
    dim_delta['t'] = nt
    for k, v in dict_vars.items():
        namdimout = tuple('t')+v
        dimout = tuple([dim_delta[k] for k in namdimout])
        ds[k] = (namdimout, np.zeros(shape=dimout, dtype=np.float32))
    return ds


def add_delta(param_delta, cc, dir_out, dtag):
    """ 
    Make the sum of deltas
    """
    from combine_delta.utils import format_dtag, join_st

    param, dict_vars, dim_delta, keys_delta_param = param_delta
    config = param['_VALID4ALL']['config']
    vnam = ''.join([k for k in dict_vars.keys()])
    dtagfrmt = format_dtag(dtag)
    fout = os.path.join(dir_out, join_st(config, 'DELTA', vnam, dtagfrmt, st='_')+'.nc')

    T0 = time.time()
    # Initialization of ds (full 0)
    ds = init_ds(1, dict_vars, dim_delta)
    for k in keys_delta_param:
        tag = param[k]['tag']
        if tag == 'MROA':
            dtg = dtag
        elif tag == 'BIAS':
             dtg = cc

        ds_t = loader_delta(dtg, param[k],
                            dict_vars, dim_delta)
        # Weighted with ncyc_wght mod[oo:1 ; iau:default yaml value]
        for var, _ in dict_vars.items():
            tweight = 1/param[k]['ncyc_wght']
            ds[var] += tweight*ds_t[var]

    print("save %s" %fout, flush=True)
    # Update encoding attrs for compression (level 1)
    encode = {'zlib': True, 'complevel': 1}
    for var, _ in dict_vars.items():
        ds[var].encoding.update(encode)
    ds.to_netcdf(fout, unlimited_dims='t')
    del ds
    T1 = time.time()
    print("elapsed time: %.1f sec" %(T1-T0), flush=True)


def loader_delta(dtg, dict_param, dict_vars, dim_delta):
    """
    Loads deltas and format variables.
    """

    from combine_delta.utils import join_st, rename_dim

    dimout = ('t', 'z', 'y', 'x')

    directory = dict_param['dir']
    tag = dict_param['tag']

    ds = init_ds(1, dict_vars, dim_delta)

    yyyy = dtg[:4]
    mm = dtg[4:6]
    dd = dtg[6:]
    dtg_regexp = join_st(yyyy, mm, dd)

    # Loop on all variables
    for v in dict_vars.keys():

        var_name = dict_param['nam_'+v]
        base_fname = dict_param['fnam_'+v]

        # If variable does not exist in delta, ds[v] = 0
        if var_name != 'None' and base_fname != 'None':
            flist = glob.glob(os.path.join(directory, base_fname+'*'+dtg_regexp+'*nc'))
            n_files = len(flist)
            if n_files != 1:
                print("flist = "+flist)
                raise RuntimeError('You should have one (just one) file in this list!')

            delta = xr.open_dataset(flist[0], chunks={}, engine='netcdf4')

            da = delta[var_name].squeeze()
            da = rename_dim(da, dimout)
            da = da.expand_dims(dim='t', axis=0)
            ds[v] = da.astype(np.float32).load()

    return ds

