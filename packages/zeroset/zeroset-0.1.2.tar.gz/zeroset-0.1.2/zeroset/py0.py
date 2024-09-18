# py basic advanced util functions
import os, sys
import inspect
import numpy as np
from tabulate import tabulate
import urllib.parse
import math
import pickle
from typing import *


def print_table(*args, tablefmt="simple_grid", no_print=False) -> str:
    """
    print table format
    :param args: same as python's print args
    :param tablefmt: tabulate's tablefmt
    :param no_print: not print if True
    :return: printed string
    """

    def parse_dict(name, d):
        return [[f'{name}["{k}"]', v] for k, v in d.items()]

    variable_names = []  # variable name, value,
    for k, v in inspect.currentframe().f_back.f_locals.items():
        variable_names.append([k, v])
        if isinstance(v, dict):
            variable_names += [e for e in parse_dict(k, v)]
    table = []
    for arg in args:
        # variable_name = [k for k, v in inspect.currentframe().f_back.f_locals.items() if v is arg]
        variable_name = [e[0] for e in variable_names if e[1] is arg]
        variable_name = variable_name[-1] if len(variable_name) > 0 else "CONSTANT"
        # if isinstance(arg, np.ndarray):
        #     print(f'{variable_name} (type={type(arg).__name__},shape={arg.shape})\n{arg}')
        # else:
        #     print(f'{variable_name} (type={type(arg).__name__}): {arg}')
        if isinstance(arg, np.ndarray):
            typename = f'{type(arg).__name__}\n - shape: {arg.shape}'
            val = arg
        elif isinstance(arg, list):
            typename = f'{type(arg).__name__}\n - len: {len(arg)}'
            val = str(arg)
            line_length = 100
            val = "\n".join([val[i:i + line_length] for i in range(0, len(val), line_length)])
        else:
            typename = type(arg).__name__
            val = arg
        table.append([variable_name, typename, val])
    headers = ["Variable", "Type", "Value"]
    print_string = tabulate(table, headers=headers, tablefmt=tablefmt)
    if not no_print:
        print(print_string)
    return print_string


def print_with_name(*args, no_print=False) -> List[str]:
    """
    print name and value
    :param args: same as python's print args
    :param no_print: not print if True
    :return: printed string
    """

    def parse_dict(name, d):
        return [[f'{name}["{k}"]', v] for k, v in d.items()]

    variable_names = []  # variable name, value,
    for k, v in inspect.currentframe().f_back.f_locals.items():
        variable_names.append([k, v])
        if isinstance(v, dict):
            variable_names += [e for e in parse_dict(k, v)]
    printed_strings = []
    for arg in args:
        variable_name = [e[0] for e in variable_names if e[1] is arg]
        variable_name = variable_name[-1] if len(variable_name) > 0 else "CONSTANT"
        print_string = f'{variable_name}: {arg}'
        if not no_print:
            print(print_string)
        printed_strings.append(print_string)
    return printed_strings


def list_chunk(lst: List, n: int):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def url_decode(text_encoded):
    return urllib.parse.unquote(text_encoded.replace("+", "%20"))


def _format_file_size(size_bytes: int, precision: int = 2, padding: str = ''):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, precision)
    return f'{s}{padding}{size_name[i]}'


def get_value_size(val):
    # 이거 dict 는 제대로 측정을 못하는데 pickle로 dumps 하고 측정해야 할듯
    return _format_file_size(sys.getsizeof(pickle.dumps(val)))


def get_file_size(file):
    return _format_file_size(os.path.getsize(file))


if __name__ == '__main__':
    arr = np.random.random((2, 3))
    d = {
        "a": 1,
        "b": 2,
        "c": 3,
        "x": {
            "y": 777,
            "z": 888
        }
    }
    c = 666
    lst = [1, 2, 3] * 50
    lst2 = [[1, 2], [3, 4], [5, 6]] * 50

    print_function = print_with_name

    print_function(arr)
    print_function(c)
    print_function(d["a"])
    print_function(d)
    print_function(d["x"])
    print_function(arr, c, d["b"], d)
    print_function(lst2)
