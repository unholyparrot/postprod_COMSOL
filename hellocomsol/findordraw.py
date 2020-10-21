"""
This block provides manipulations with DataFrame, 
such as finding the maximum or making plots. 
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.integrate import simps
from tqdm.auto import tqdm


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


def get_extr_df(df, var_p, time_slice=1, func_type="max"):
    """
    Finds the extremum (maximum by default) of the variable at each time point of the whole time array.
    :param df: DataFrame with values
    :param var_p: variable for the max search
    :param time_slice: use it if you don't need each time point, does exactly `time[::time_slice]`
    :param func_type: max or min function
    :return: new DataFrame with max/min information
    """
    if func_type == "max":
        func = lambda x_df: x_df.idxmax()
    elif func_type == "min":
        func = lambda x_df: x_df.idxmin()
    else:
        raise ValueError("Unknown func_type argument {}".format(func_type))
    v_max_df = pd.DataFrame()
    for t_step in df.t.unique()[::time_slice]:
        at_t = df[df.t == t_step].reset_index()
        max_row = at_t.iloc[func(at_t[var_p])]
        v_max_df = v_max_df.append(max_row)
        
    return v_max_df


def integrate_var(df, cutline, as_cutline='x', as_y='fn(mol/m^3)', as_x='y', as_param='t'):
    """
    Integrates the values from DataFrame. 
    :param df: DataFrame with values
    :param cutline: ndarray with valeus of the cutline
    :param as_y: heading of the column with the values for the integration
    :param as_x: heading of the column as the axis for the integration
    :param as_param: heading of the column with the values of the parametr
    :param as_cutline: heading of the cutline column
    :return: (cutline.size, df[as_param].unique().size) ndarray with integration results
    """
    along_param = df[as_param].unique()
    I_keeper = np.empty((cutline.size, along_param.size))
    for i, cut in enumerate(tqdm(cutline, desc="Cutline loop")):
        for j, param in enumerate(along_param):
            at_tx = df[(df[as_cutline] == cut) & (df[as_param] == param)]
            x = at_tx[as_x]
            y = at_tx[as_y]
            I_keeper[i][j] = simps(y, x)
    
    return I_keeper
