import syslog


def to_gb(bytes):
  BYTES_IN_MEGABYTE = 1048576
  BYTES_IN_GIGABYTE = BYTES_IN_MEGABYTE * 1000
  # BYTES_IN_GIGABYTE = 1073741824

  return int(bytes) / BYTES_IN_GIGABYTE


def log(message):
  syslog.syslog(syslog.LOG_DEBUG, message)
