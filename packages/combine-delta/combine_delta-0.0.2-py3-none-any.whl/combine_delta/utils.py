#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  26 10:06:00 2023

@author: mhamon

"""

import pandas as pd
import xarray as xr
import numpy as np


def format_dtag(dtg):
    """ Formats YYYYMMDD string to yYYYYmMMdDD."""

    yyyy = dtg[:4]
    mm = dtg[4:6]
    dd = dtg[6:]
    return 'y'+yyyy+'m'+mm+'d'+dd


def join_st(*args, st='*'):
    """ Joins args arguments with st argument."""
    return st.join(list(args))

def rename_dim(da, dimout):
    """ Renames dimensions. """

    dimin = get_dim_name(da)
    for d in dimout:
        try:
            da = da.rename({dimin[d]:d})
        except ValueError:
            pass
    return da


def get_dim_name(f):
    """
    Get dimension information from a dataset f.

    """

    import re

    dimx = ''; dimy = ''; dimz = ''; dimt = ''

    dim = {}
    dim['x'] = pick_first([dd for dd in f.dims if (re.search('x',dd,re.I)
                                                or re.search('lon',dd,re.I))
                                                and not re.search('axis',dd,re.I)])
    dim['y'] = pick_first([dd for dd in f.dims if (re.search('y',dd,re.I)
                                                or re.search('lat',dd,re.I))
                                                and not re.search('axis',dd,re.I)])
    dim['z'] = pick_first([dd for dd in f.dims if (re.search('z',dd,re.I)
                                                or re.search('depth',dd,re.I)
                                                or re.search('lev',dd,re.I))
                                                and not re.search('axis',dd,re.I)])
    dim['t'] = pick_first([dd for dd in f.dims if (dd == 't')
                                                or re.search('tim',dd,re.I)
                                                and not re.search('axis',dd,re.I)])

    return dim

def pick_first(iterable):
    """
    Returns the first element of a list if len(list)>0, otherwise returns the list.

    """

    if len(iterable) > 0:
        return iterable[0]
    else:
        return ''


def AddDay_pd(pddate: pd.Timestamp or str, nbd: int, forcefmt: bool = True) -> pd.Timestamp or str:
    """
    Add days to a gregorian date.

    :param pddate: Gregorain date (pd.Timestamp or str).
    :param nbd:  Number of days to add to pddate.
    :param forcefmt: Boolean, force formatting output to the input format.

    """

    ln_str = False
    if isinstance(pddate, str):
        ln_str = True
        pddate =  pd.to_datetime(pddate)

    outdate = pddate + pd.Timedelta(nbd, unit='D')

    if ln_str and forcefmt:
        YYYY = '%04d'%outdate.year
        MM = '%02d'%outdate.month
        DD = '%02d'%outdate.day
        outdate = YYYY+MM+DD

    return outdate

def load_param(param_file, id_ana, dir_in, mod):
    """
    Loads yaml parameter file.

    warning:
        It can add/modify some parameters in the output dictionnary
        depending on id_ana/dir_in/mod arguments.
    """

    import yaml
    from py4ease.interfaces.iyaml import construct_loader

    dict_dims = {}
    dict_dims[2] = ('y', 'x')
    dict_dims[3] = ('z', 'y', 'x')

    with open(param_file, "r") as f:
        param = list(yaml.load_all(f, Loader=construct_loader()))[0]

    dim_delta = {}
    dim_delta['z'] = param['_VALID4ALL']['nz']
    dim_delta['y'] = param['_VALID4ALL']['nj']
    dim_delta['x'] = param['_VALID4ALL']['ni']

    namtag = 'nam_'
    deltavars = [k.split(namtag)[1] for k in param['_VALID4ALL'].keys() if k.startswith(namtag)]
    dimtag = 'dim_'
    dimvars = [int(param['_VALID4ALL'][dimtag+dv]) for dv in deltavars]
    dict_vars = {dv:dict_dims[nd]  for dv, nd in zip(deltavars, dimvars)}

    keys_delta_param = [k for k in param.keys() if k.startswith('delta')]

    n_ana_param = len(keys_delta_param)
    assert len(id_ana) <= n_ana_param
    # Select only n_ana parameters
    keys_delta_param = ['delta_'+ii for ii in id_ana if ii!="None"]
    assert all([k in param.keys() for k in keys_delta_param])

    # Add dir_in for each delta in param
    for ik, k in enumerate(keys_delta_param):
        param[k]['dir'] = dir_in[ik]
        if mod == 'oo':
            # Force ncyc_wght to 1 in oo mode only
            param[k]['ncyc_wght'] = 1

    return param, dict_vars, dim_delta, keys_delta_param

