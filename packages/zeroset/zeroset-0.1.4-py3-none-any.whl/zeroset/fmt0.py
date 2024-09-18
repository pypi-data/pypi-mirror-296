import math


def format_file_size(size_bytes: int, precision: int = 2, padding: str = ''):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, precision)
    return f'{s}{padding}{size_name[i]}'


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
