from . import LOG_FILENAME
import logging
import sys


# set up formatting
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

# set up logging to STDOUT for all levels DEBUG and higher
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)

# set up logging to a file for all levels DEBUG and higher
fh = logging.FileHandler(LOG_FILENAME)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# create Logger object
mylogger = logging.getLogger('MyLogger')
mylogger.setLevel(logging.DEBUG)
mylogger.addHandler(sh)
mylogger.addHandler(fh)

# create shortcut functions
debug = mylogger.debug
info = mylogger.info
warning = mylogger.warning
error = mylogger.error


