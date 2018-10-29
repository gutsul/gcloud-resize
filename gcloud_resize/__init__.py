__version__ = '0.9.4'
name = "gcloud-resize"

CONF_DIR = "/etc/{}".format(name)
CONFIG_FILENAME = "{0}/{1}.conf".format(CONF_DIR, name)

LOG_DIR = "/var/log/{}".format(name)
LOG_FILENAME = "{0}/{1}.log".format(LOG_DIR, name)
LOG_MAX_BYTES = 1048576
LOG_BACKUP_COUNT = 5