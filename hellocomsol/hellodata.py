"""
This block provides manipulations with the data,
such as reading from file into DataFrame and making output CSV.
"""
import os
import numpy as np
import pandas as pd
from tqdm import tqdm


# TODO: сделать нормальное взаимодействие с output
def make_csv(df, filename, output=''):
    """
    Makes the csv
    :param df: from DataFrame
    :param filename: full path
    :param output: probably output path
    :return:
    """
    f_name, _ = os.path.splitext(filename)
    df.to_csv(output + '{}_new_df.csv'.format(os.path.basename(f_name)), index=False)


def read_from_csv(filename):
    """
    We use it if there it is a csv file already instead of reading COMSOL export.
    :param filename: path to the csv file
    :return: pandas.DataFrame
    """
    print("Reading from csv file into DataFrame.")
    df = pd.read_csv(filename).reset_index().iloc[:, 1:]
    print("Reading from file is done.")
    return df


def get_data_frame(filename):
    """
    Reads and parses the COMSOL export file to return pandas.DataFrame with values.
    At this moment can read only one type of output with columns in specified order;
        [time, x, y, velocity, shear rate, thrombin concentration,
        fibrin concentration, fibrinogen concentration]
    :param filename: name of the data file
    :return: pandas.DataFrame
    """
    df = pd.DataFrame(columns=["t", "x", "y", "U", "sr", "thr", "fn", "fg"])
    with open(filename, 'r') as f_data:
        # skipping the heading
        for _ in range(9):
            next(f_data)
        # beautiful status bar is available now
        for line in tqdm(f_data.readlines(), desc=filename):
            if line:
                bs = line.split()
                if len(bs) >= 1:
                    x = np.tile(np.array([bs[0]], dtype=np.float32), 101)
                    y = np.tile(np.array([bs[1]], dtype=np.float32), 101)
                    time = np.arange(0, 10.1, 0.1, dtype=np.float32)
                    values = np.array([time, x, y, bs[2::5], bs[3::5], bs[4::5], bs[5::5], bs[6::5]],
                                      dtype=np.float32).T
                    dft = pd.DataFrame(values, columns=["t", "x", "y", "U", "sr", "thr", "fn", "fg"])
                    df = pd.concat([df, dft])
            else:
                break
    df = df.reset_index().iloc[:, 1:]
    return df
