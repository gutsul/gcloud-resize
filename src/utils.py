import os
import syslog

import sys
from psutil._common import usage_percent, sdiskusage
from psutil._compat import PY3, unicode


def to_gb(bytes):
  BYTES_IN_MEGABYTE = 1048576
  BYTES_IN_GIGABYTE = BYTES_IN_MEGABYTE * 1000

  return int(bytes) / BYTES_IN_GIGABYTE


def disk_usage(path):
  try:
    st = os.statvfs(path)
  except UnicodeEncodeError:
    if not PY3 and isinstance(path, unicode):
      # this is a bug with os.statvfs() and unicode on
      # Python 2, see:
      # - https://github.com/giampaolo/psutil/issues/416
      # - http://bugs.python.org/issue18695
      try:
        path = path.encode(sys.getfilesystemencoding())
      except UnicodeEncodeError:
        pass
      st = os.statvfs(path)
    else:
      raise
  free = (st.f_bavail * st.f_frsize)
  total = (st.f_blocks * st.f_frsize)
  used = (st.f_blocks - st.f_bfree) * st.f_frsize
  percent = usage_percent(used, total, _round=1)
  # NB: the percentage is -5% than what shown by df due to
  # reserved blocks that we are currently not considering:
  # http://goo.gl/sWGbH
  return sdiskusage(total, used, free, percent)


def log(message):
  syslog.syslog(syslog.LOG_DEBUG, message)
