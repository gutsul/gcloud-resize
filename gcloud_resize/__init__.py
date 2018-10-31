from os.path import expanduser

__version__ = '0.9.7'
name = "gcloud-resize"

HOME = expanduser("~")
APP_HOME= "{home}/.{name}".format(home=HOME, name=name)
CONFIG = "{home}/{name}.conf".format(home=APP_HOME, name=name)

LOG_DIR = "{home}/logs".format(home=APP_HOME)
LOG_FILE = "{log_dir}/{name}.log".format(log_dir=LOG_DIR, name=name)
LOG_MAX_BYTES = 1048576
LOG_BACKUP_COUNT = 5