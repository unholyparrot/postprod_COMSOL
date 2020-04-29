#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from hellocomsol import hellodata, arg_and_path
import sys
import os


def main():
    # reading the input
    f_name = arg_and_path.setup_args().input
    # removing the index column from error parsing
    df = hellodata.read_from_csv(f_name)
    df = df.drop(columns='Unnamed: 0')
    hellodata.make_csv(df, f_name)


if __name__ == '__main__':
    main()
