"""
This block provides all the manipulations with the data,
such as reading from file, making output csv and plots.
"""
import os
import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


# TODO: сделать нормальное взаимодействие с output
def make_csv(df, filename, output=''):
    """
    Makes the csv
    :param df: from DataFrame
    :param filename: full path
    :param output: probably output path
    :return:
    """
    f_name, f_ex = os.path.splitext(filename)
    df.to_csv(output + '{}_new_df.csv'.format(os.path.basename(f_name)), index=False)
    print("CSV is done: " + output + '{}_new_df.csv'.format(os.path.basename(f_name)))


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
        for line in tqdm.tqdm(f_data.readlines(), desc=filename):
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


def get_time(df, time=10):
    """
    Selects only points with t = time from the df, resets the index.
    :param df: pandas.DataFrame with COMSOL export
    :param time: time for selection
    :return: pandas.DataFrame where t = time
    """
    df_at_time = df[(df['t'] == time)].reset_index().iloc[:, 1:]
    return df_at_time


def interpolate_values(df, variable='U', inter_num=1000):
    """
    Interpolates values for variable from df to inter_num*inter_num number of points
    :param df: pandas.DataFrame with values
    :param variable: variable for interpolation
    :param inter_num: number of points for the interpolation mesh
    :return: three 2D arrays; grid_x and grid_y as the mesh, int_data as the interpolated values
    """
    x = df['x'].values
    y = df['y'].values
    z = df[variable].values

    # values for interpolation
    x_new = np.linspace(x.min(), x.max(), num=inter_num)
    y_new = np.linspace(y.min(), y.max(), num=inter_num)

    grid_x, grid_y = np.meshgrid(x_new, y_new)

    # we use ravel to make N*N points for interpolation
    # that gives us the all points from the grid, not only the diagonal
    int_data = griddata(np.array([x, y]).T, z, (grid_x.ravel(), grid_y.ravel()), method='cubic')

    return grid_x, grid_y, int_data.reshape(inter_num, inter_num)


# TODO: нужно изменить границы colorbar для графиков скорости сдвига
# TODO: нужно добавить считывание файла-конфигуратора для изменения масштаба и подписей
def draw_interpolated(grid_x, grid_y, grid_z, output, variable='U', time=10):
    """
    Takes the interpolated data to make a colormap. Doesn't show the plot, but saves it.
    :param grid_x: grid for x
    :param grid_y: grid for y
    :param grid_z: grid for interpolated values
    :param output: output directory for saving the picture
    :param variable: variable for the title. It can differ from the headings of the DataFrame
    :param time: time for the title.
    :return: nothing, but makes a plot.
    """
    plt.figure(figsize=(18, 6))
    plt.pcolormesh(grid_x, grid_y, grid_z)
    plt.colorbar()

    plt.xlim(-5e-5, 145e-5)
    plt.ylim(-5e-6, 55e-6)
    plt.xlabel('x, m')
    plt.ylabel('y, m')
    plt.title('{0} at t={1}'.format(variable, time))
    plt.savefig(output + '/{0}_at_{1}s.png'.format(variable, time),
                dpi=80, pad_inches=1.5, bbox_inches='tight')
    plt.close()
