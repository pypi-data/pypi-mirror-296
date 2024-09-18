# from zeroset import py0
# import numpy as np
# import sys
#
# a = np.zeros((300, 300, 3), dtype=np.uint8)
#
# print(py0.get_value_size(a))
#
# print(py0._format_file_size(sys.getsizeof(a)))

from zeroset import log0
import logging

logging.debug('This message is a log message.')
logging.info('This message is a log message.')
logging.warning('This message is a log message.')
logging.error('This message is a log message.')
logging.critical('This message is a log message.')
