#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hellodata
import arg_and_path
import sys
import os


def main():
    # Reading arguments
    args = arg_and_path.setup_args()

    # Here we check the input and output directory
    arg_and_path.check_input(args.input)
    output = arg_and_path.check_output(args.output)
    # Here we print how did the script understood the commands
    print('Found time points: ' + ', '.join(map(str, args.time)))
    print('Found variables: ' + ', '.join(args.variable))

    # Here we check the extension of input file to make a decision
    in_filename, in_extension = os.path.splitext(args.input)
    if in_extension == '.csv':
        # We just read csv and do not waste time for parsing txt
        df = hellodata.read_from_csv(args.input)
    elif in_extension == '.txt':
        # We should parse the data and get the DataFrame
        df = hellodata.get_data_frame(args.input)
        # Saving as csv for future
        df.to_csv(output + '/{}_df.csv'.format(os.path.basename(in_filename)))
        print('    df.csv for future is done.')
    else:
        # We should avoid an other extensions
        print("Error input format.")
        sys.exit("Closing...")

    print("Making pictures...")
    # Processing all the time points
    for curr_time in args.time:
        df_t = hellodata.get_time(df, curr_time)
        # Processing all the variables
        for curr_variable in args.variable:
            grid_x, grid_y, grid_z = hellodata.interpolate_values(df_t, curr_variable)
            hellodata.draw_interpolated(grid_x, grid_y, grid_z, output, curr_variable, curr_time)

    print("Done successfully.")


if __name__ == '__main__':
    main()
