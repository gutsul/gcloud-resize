import syslog


def no_dimen(line):
  return line[:-1]


def log(message):
  syslog.syslog(syslog.LOG_DEBUG, message)

