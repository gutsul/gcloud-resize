import logging.handlers
from . import LOG_FILENAME, name
#
# logger = logging.getLogger(name=name)
#
# handler = logging.handlers.RotatingFileHandler(
#   log_path, maxBytes=1000000, backupCount=5)
#
# logger.addHandler(handler)
#
# # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#
#
# logger.debug("Test debug message")
# logger.info("Test info message")
# logger.error('Error message')
# logger.critical('Critical message')

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
critical = mylogger.criticale