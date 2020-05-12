#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tqdm
from hellocomsol import hellodata, arg_and_path


def main():
    # reading the input
    args = arg_and_path.setup_args()
    if args.remove:
        print("Input files will be removed after making the CSV")
    # as the nargs function is available now
    f_names = args.input
    for f_name in tqdm.tqdm(f_names, desc='Total progress'):
        df = hellodata.get_data_frame(f_name)
        hellodata.make_csv(df, f_name)
        # if I want to remove the input after making a csv
        if args.remove:
            os.remove(f_name)
            print("{} was removed".format(f_name))


if __name__ == '__main__':
    main()
