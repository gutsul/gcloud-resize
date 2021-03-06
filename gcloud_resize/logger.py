from logging.handlers import RotatingFileHandler

from . import LOG_FILE, LOG_MAX_BYTES, LOG_BACKUP_COUNT
import logging

# set up formatting
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

# set up logging to a file for all levels DEBUG and higher
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# create Logger object
mylogger = logging.getLogger('MyLogger')
mylogger.setLevel(logging.DEBUG)
mylogger.addHandler(file_handler)

# create shortcut functions
debug = mylogger.debug
info = mylogger.info
warning = mylogger.warning
error = mylogger.error


