# py basic advanced util functions
from dataclasses import dataclass
from enum import Enum, auto
import os, sys
import inspect
import numpy as np
from tabulate import tabulate
import urllib.parse
import math
import pickle
import json
from typing import *

python_print = print


@dataclass(frozen=True)
class TableFormat(Enum):
    plain = auto()
    simple = auto()
    github = auto()
    grid = auto()
    simple_grid = auto()
    rounded_grid = auto()
    heavy_grid = auto()
    mixed_grid = auto()
    double_grid = auto()
    fancy_grid = auto()
    outline = auto()
    simple_outline = auto()
    rounded_outline = auto()
    heavy_outline = auto()
    mixed_outline = auto()
    double_outline = auto()
    fancy_outline = auto()
    pipe = auto()
    orgtbl = auto()
    asciidoc = auto()
    jira = auto()
    presto = auto()
    pretty = auto()
    psql = auto()
    rst = auto()
    mediawiki = auto()
    moinmoin = auto()
    youtrack = auto()
    html = auto()
    unsafehtml = auto()
    latex = auto()
    latex_raw = auto()
    latex_booktabs = auto()
    latex_longtable = auto()
    textile = auto()
    tsv = auto()

    def __str__(self):
        return self.name


########## print #####

class print:
    @staticmethod
    def print_table(*args, tablefmt: Union[str, TableFormat] = TableFormat.simple_grid, no_print: bool = False) -> str:
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
        if not isinstance(tablefmt, str):
            tablefmt = str(tablefmt)
        print_string = tabulate(table, headers=headers, tablefmt=tablefmt)
        if not no_print:
            python_print(print_string)
        return print_string

    @staticmethod
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
                python_print(print_string)
            printed_strings.append(print_string)
        return printed_strings

    @staticmethod
    def print_auto(*args, cr=False):
        """
        Automatically prints depending on the variable type.
        :param args: variables
        :param cr: carriage return. If this value is True, the list is output one per line.
        """
        for arg in args:
            if isinstance(arg, list):
                if cr is False:
                    python_print(arg)
                else:
                    python_print(*arg, sep="\n")
            elif isinstance(arg, dict):
                python_print(json.dumps(arg, indent=2, ensure_ascii=False))
            elif isinstance(arg, np.ndarray):
                python_print(arg.tolist())
            else:
                python_print(arg)


##########

def list_chunk(lst: List, n: int):
    """
    Returns a list split into N length chunks.
    :param lst: 1 dimensional list
    :param n: chunk size
    :return:
    """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def merge_dict(dict_chunks: List[dict]):
    merged_dict = {}
    for data in dict_chunks:
        merged_dict.update(data)
    return merged_dict


def get_url(host, params):
    return host + "?" + "&".join([f'{k}={v}' for k, v in params.items()])


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
    try:
        return _format_file_size(len(pickle.dumps(val, protocol=pickle.HIGHEST_PROTOCOL)))
    except Exception as e:
        try:
            return f"{_format_file_size(sys.getsizeof(val))} (approximate)"
        except Exception:
            return "Size unknown"


def get_file_size(file):
    return _format_file_size(os.path.getsize(file))


def get_base_name(file):
    return os.path.splitext(os.path.basename(file))[0]


def ms_to_hms(milliseconds):
    hour = milliseconds // 3600000
    milliseconds %= 3600000
    minute = milliseconds // 60000
    milliseconds %= 60000
    second = milliseconds // 1000
    milliseconds %= 1000
    return hour, minute, second, milliseconds


def s_to_hms(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return hour, minutes, seconds


def pretty_dumps(data, indent=None, precision=None):
    import re
    if precision is None:
        output = json.dumps(data, indent=indent, sort_keys=True)
    else:
        output = json.dumps(json.loads(json.dumps(data), parse_float=lambda obj: round(float(obj), precision)), indent=indent, sort_keys=True)

    def flat_list(match):
        elems = [e.strip() for e in match.group(0).split("\n") if len(e.strip()) != 0]
        return elems[0] + " ".join(elems[1:])

    output = re.sub('\[([^\]]+)', flat_list, output)
    return output


if __name__ == '__main__':
    # headers = ["Planet", "R (km)", "mass (x 10^29 kg)"]
    # table = [["Sun", 696000, 1989100000], ["Earth", 6371, 5973.6], ["Moon", 1737, 73.5], ["Mars", 3390, 641.85]]
    #
    # for format in TableFormat.__members__:
    #     print(f'### {format.lower()}')
    #     print("```")
    #     print(tabulate(table, headers, tablefmt=format.lower()))
    #     print("```")
    #     print()
    # exit()
    arr = np.random.random((2, 3))
    arr_large = np.random.random((20000, 10000))
    c = 666
    lst = [1, 2, 3] * 50
    lst2 = [[1, 2], [3, 4], [5, 6]] * 5
    d = {
        "a": 1,
        "b": 2,
        "c": 3,
        "x": {
            "y"  : 777,
            "z"  : 888,
            "arr": lst,
            "ttt": {
                "abc": lst2,
                "k"  : 999
            }
        },

    }
    # print.print_auto(d)
    python_print(pretty_dumps(d, indent=2))
    exit()
    import pprint

    pp = pprint.PrettyPrinter(indent=2, width=500, compact=False)
    pp.pprint(d)
    # print_function = print.print_table
    #
    # print_function(arr)
    # print_function(c)
    # print_function(d["a"])
    # print_function(d)
    # print_function(d["x"])
    # print_function(arr, c, d["b"], d)
    # print_function(lst2)
