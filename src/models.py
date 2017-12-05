import math
import os
import sys

from psutil._common import usage_percent, sdiskusage
from psutil._compat import PY3, unicode

from settings import FREE_LIMIT_PERCENT, RESIZE_PERCENT
from src import utils


class Disk:
  name = None
  index = 0
  mount_point = None

  def __init__(self, name, index):
    self.name = name
    self.index = index

  def get_label(self):
    result = "sd" + chr(97 + self.index)
    return result

  def usage(self):
    """Return disk usage associated with path."""

    path = self.mount_point

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

  def is_low(self):
    usage = self.usage()
    free_gb = utils.to_gb(usage.free)
    free_percent = 100 - usage.percent

    if free_percent < FREE_LIMIT_PERCENT:
      print('DEBUG: ACTION="Low disk" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}" FREE_GB={3} USED_%={4}'
            .format(self.get_label(), self.name, self.mount_point, free_gb, usage.percent))
      return True
    else:
      return False

  def cal_new_size_gb(self):
    usage = self.usage()

    total_gb = math.ceil(utils.to_gb(usage.total))
    add_size_gb = math.ceil((RESIZE_PERCENT / 100) * total_gb)
    new_size_gb = total_gb + add_size_gb

    print('DEBUG: ACTION="New disk size" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}" ADD_GB={3} NEW_SIZE_GB={4}'
          .format(self.get_label(), self.name, self.mount_point, add_size_gb, new_size_gb))

    return new_size_gb