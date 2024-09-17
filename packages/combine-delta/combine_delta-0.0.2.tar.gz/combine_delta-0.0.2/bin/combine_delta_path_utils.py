#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Tue Jan  24 10:30:00 2023

@author: mhamon

"""


def path():
    "Returns combine_delta installation path"

    import combine_delta
    path_cmb = combine_delta.__path__[0]
    print(path_cmb)

