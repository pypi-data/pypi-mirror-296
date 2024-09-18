import inspect
import os
import sys

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
sys.path.append(real_path)

try:
    import zeroset.cv0 as cv0
    import zeroset.py0 as py0
    import zeroset.log0 as log0
    from zeroset.log0 import ColoredLogHandler
    import logging
except ImportError as e:
    print(e, "Import Error")
    exit(1)

__all__ = [name for name, obj in locals().items()
           if not (name.startswith('_') or inspect.ismodule(obj))]

# cv0: Extended version for cv2
# fmt0 : Extended format convert functions
# l0: colored log
# py0: make python function more easier
# s0 : selenium
# v0 : about visualization
