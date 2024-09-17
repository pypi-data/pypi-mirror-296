#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  30 21:27:00 2023

@author: mhamon

Combine_delta

The purpose of this program is to sum different correction (MROA, BIAS).
"""

import os
from mpi4py import MPI

import pandas as pd
import xarray as xr
import numpy as np

import multiprocessing

try:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    procs = np.arange(size)
    force_deactivate_mpi=False

except:
    force_deactivate_mpi=True


def main():
    """
    main program
    
    Reads input arguments and launch processes. 

    """

    from combine_delta.get_args import get_args
    from combine_delta.utils import AddDay_pd, load_param
    from combine_delta.delta import add_delta

    args = get_args()

    # List of days of the cycle
    ldays_seek = [AddDay_pd(args.cycl, dd+1) for dd in range(-args.l, 1, 1)]
    # Reads the yaml parameter file
    param_delta = load_param(args.param, args.id_ana, args.dir_in, args.mod)

    # Launch one process per day
    dict_vars = param_delta[1]

    nkeys = len(dict_vars)
    ld = len(ldays_seek)
    nbprocess = nkeys*ld
    list_ldays_seek = ldays_seek*nkeys
    list_var = []
    for l in list(dict_vars.keys()):
        list_var += [l]*ld

    # MPI implementation (faster)
    if args.v == 'mpi' and not force_deactivate_mpi:
        wrk = [int(spl[0]) for spl in np.array_split(procs, nbprocess)]
        # A task for each day and var
        for iw, iday, iv in zip(wrk, list_ldays_seek, list_var):
            if rank == iw:
                dv = {iv: dict_vars[iv]}
                prmd = (param_delta[0], dv, param_delta[2], param_delta[3])
                print("rank %s, add_delta(param_delta, args.cycl, args.dir_out, %s) for var %s" %(rank, iday, iv))
                add_delta(prmd, args.cycl, args.dir_out, iday)

    # Multiprocess implemtation (slower)
    elif args.v == 'multiprocess':
        prmd = [[] for i in range(len(list_var))]
        cc = [[] for i in range(len(list_var))]
        do = [[] for i in range(len(list_var))]
        for iv, var in enumerate(list_var):
            dv = {var: dict_vars[var]}
            prmd[iv] = (param_delta[0], dv, param_delta[2], param_delta[3])
            cc[iv] = args.cycl
            do[iv] = args.dir_out
        pool = multiprocessing.Pool(processes=len(list_var))
        pool.starmap(add_delta, zip(prmd, cc, do, list_ldays_seek))
        pool.close()



if __name__ == '__main__':
    main()
    if not force_deactivate_mpi:
        MPI.Finalize()
