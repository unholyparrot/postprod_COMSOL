"""
This block provides argument parsing,
checking the paths of input and output.
"""
import argparse
import os
import sys


def setup_args():
    parser = argparse.ArgumentParser(description="Post processing of COMSOL export")

    parser.add_argument('-in',
                        '--input',
                        nargs='+',
                        help='Input file(s) with COMSOL export',
                        type=str,
                        required=True)

    parser.add_argument('-v',
                        '--variable',
                        nargs='+',
                        help='Variable(s) for plotting',
                        type=str,
                        required=False)

    parser.add_argument('-t',
                        '--time',
                        nargs='+',
                        help='Time point(s) for plotting',
                        type=float,
                        required=False)

    parser.add_argument('-o',
                        '--output',
                        help='Output directory',
                        type=str,
                        required=False)

    parser.add_argument('-rm',
                        '--remove',
                        help='Flag for removing input TXT after making CSV',
                        action='store_true',
                        default=True,
                        required=False,
                        )

    return parser.parse_args()


def check_input(path):
    try:
        if os.path.exists(path):
            print("Found input: {}".format(path))
        else:
            print("Found no input.")
            sys.exit("Closing...")
    except FileNotFoundError:
        print("Found no input.")
        sys.exit("Closing...")


def make_directory(path):
    try:
        os.mkdir(path)
        print("Output path: {}".format(path))
    except FileExistsError:
        print("No access to the directory or something else.")


def check_output(path):
    if path:
        if os.path.exists(path):
            print("Found output path: {}".format(path))
        else:
            make_directory(path)
        return path
    else:
        make_directory(os.getcwd() + '/output')
        return os.getcwd() + '/output'
