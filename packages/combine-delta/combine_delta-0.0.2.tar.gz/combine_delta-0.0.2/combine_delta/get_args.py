#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  26 10:06:00 2023

@author: mhamon

"""

def get_args():
    """
    Get the input arguments

    """

    import argparse
    from distutils.util import strtobool

    parser = argparse.ArgumentParser(
                   description='''Combine your deltas!''')
    parser.add_argument('--v', type=str,
                        default='mpi', choices=['mpi', 'multiprocess'],
                        help='Choose your version of combine_delta.')
    parser.add_argument('-param', type=str,
                        help='yaml file of delta parameters')
    parser.add_argument('-cycl', type=str,
                        help='tag of the cycle')
    parser.add_argument('-l', type=int,
                        help='length of the cycle')
    parser.add_argument('-id_ana', type=str, nargs='+',
                        help='ids of delta to sum (respecting yaml file order)')
    parser.add_argument('--mod', type=str,
                        default='iau', choices=['iau', 'oo'],
                        help='mode determining the way to sum deltas')
    parser.add_argument('-dir_in', type=str, nargs='+',
                        help='input directories')
    parser.add_argument('-dir_out', type=str,
                        help='output directory')

    args = parser.parse_args()

    if len(args.dir_in) != len(args.id_ana):
        raise RuntimeError('Number of dir_in argument has to be equal to the one of id_ana argument')

    return args

