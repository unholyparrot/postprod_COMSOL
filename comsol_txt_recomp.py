#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Скрипт для превращения экспорта COMSOL (txt) в csv.
"""

import argparse
import re
import datetime
import os 

from tqdm.auto import tqdm


def setup_args():
    parser = argparse.ArgumentParser(description="Process the COMSOL export to csv")

    parser.add_argument('-in',
                        '--input',
                        nargs='+',
                        help="""Path to the input file(s)
                                Example: -in /home/owl/export1.txt /home/owl/export2.txt""", 
                        type=str,
                        required=True)

    parser.add_argument('-out', 
                        '--output',
                        help="""Path to the output directory.
                                Example: -out /home/owl/output_csv""",
                        type=str,
                        required=True)
    
    return parser.parse_args()


class ParsingIterator:
    """
    Iterates over the given values_array array, 
    giving an array with the number of elements specified in num_variables as an iteration.
    :param values_array: input list
    :param num_variables: number of values per iteration
    """
    def __init__(self, values_array: list, num_variables: int):
        self.valeus_array = values_array
        self.num_variables = num_variables
        self.start = 0
        self.stop = num_variables
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.stop <= len(self.valeus_array):
            num = self.valeus_array[self.start:self.stop]
            self.start += self.num_variables
            self.stop += self.num_variables
            return num
        else:
            raise StopIteration


def count_total_rows(filename):
    """
    Function from stack overflow, counts the number of rows in the file.
    """
    def blocks(files, size=65536):
        while True:
            b = files.read(size)
            if not b: break
            yield b

    with open(filename, "r", encoding="utf-8", errors='ignore') as f:
        return sum(bl.count("\n") for bl in blocks(f))


def headings_row_parser(headings_array: list):
    """
    Parses a header describing the data structure of a COMSOL export file.
    Parameters:
        headings_array (list): an array containing the header string, split by space.
    Returns:
        coordinates_headings (list): all headings of coordinates (x, y, z, ...).
        variables_headings (list): all headings of found variables (U, v, br.sr, ...)
        params (dict): dict with found params as keys and values as values ({'t': ['1', '2', ..], ...})
    """
    coordinates_headings = list()
    variables_headings = list()
    params = dict()

    try:
        for elem in headings_array:
            if elem != '%':
                if len(elem) == 1:
                    if elem not in coordinates_headings:
                        coordinates_headings.append(elem)
                else:
                    if elem[0] != '@':
                        if elem not in variables_headings:
                            variables_headings.append(elem)
                    else:
                        params_row = elem[1:].split(',')
                        for param in params_row:
                            param_name, param_value = param.split('=')
                            if params.get(param_name) is None:
                                params[param_name] = [param_value]
                            else:
                                params[param_name].append(param_value)
            else:
                continue
    except Exception:
        print("Oops..." )
        print(elem)
    
    return coordinates_headings, variables_headings, params


def overwriting_input_data(filename, output=""):
    total_rows = count_total_rows(filename)
    with open(filename, 'r') as f_data:
        # saving the entire header of the original file
        heading = ""
        for _ in range(8):
            heading += next(f_data)
        # reading how the data is written
        headings_row = next(f_data)
        re_row = re.sub(r' \(', '(', headings_row)  # объединяем переменные с размерностями
        re_row = re.sub('@ ', '@', re_row)  # объединяем параметры с отделителем параметров
        re_row = re.sub(', ', ',', re_row)  # убираем лишние пробелы после запятых
        headings_array = re_row.split()  # парсим по пробелу
        
        # получаем количество координатных осей, переменных, параметров
        coordinates_headings, variables_headings, params = headings_row_parser(headings_array)
        # составляем из этого наименования будущих колонок csv файла 
        column_names = (','.join(params.keys()) + ',' + 
                        ','.join(coordinates_headings) + ',' + 
                        ','.join(variables_headings) + '\n')
        
        with open(output + '/parsed_{}.csv'.format(os.path.splitext(os.path.split(filename)[1])[0]), 'w') as w_data:
            # w_data.write(heading)
            w_data.write(column_names)
            # читаем ещё столько раз, сколько есть строчек с данными
            for _ in tqdm(range(total_rows - 9), desc=os.path.split(filename)[1]):
                # сразу разделяем по пробелам
                line = next(f_data).split()
                # отрезаем переменные
                coords = line[:len(coordinates_headings)]
                for couple_number, elem in enumerate(ParsingIterator(line[len(coordinates_headings):], 
                                                                     len(variables_headings))):
                    s = (','.join([params[x_param][couple_number*len(variables_headings)] for x_param in params.keys()]) + ',' +
                         ','.join(coords) + ',' + 
                         ','.join(elem) + '\n')
                    w_data.write(s)


def main():
    args = setup_args()
    with open('log_files/log_comsol_txt_recomp.txt', 'a+') as logger:
        logger.write(str(datetime.datetime.now()) + ' | argparse | {}'.format(args) + '\n')
    
    for f_name in args.input:
        overwriting_input_data(f_name, output=args.output)


if __name__ == "__main__":
    try:
        main()
        with open('log_files/log_comsol_txt_recomp.txt', 'a+') as logger:
            logger.write("__________" + '\n')
    except FileNotFoundError as er:
        print(er)
        print("Check the input/output direcory.")
        with open('log_files/log_comsol_txt_recomp.txt', 'a+') as logger:
            logger.write(str(datetime.datetime.now()) + ' | error | ' + str(er) + '\n')
            logger.write("__________" + '\n')
