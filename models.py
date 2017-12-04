import math

from settings import FREE_LIMIT_PERCENT, RESIZE_PERCENT


class Disk:
  name = None
  index = 0
  mount_point = None
  size_gb = 0
  used_size_gb = 0

  def __init__(self, name, index):
    self.name = name
    self.index = index

  def get_label(self):
    result = "sd" + chr(97 + self.index)
    return result

  def is_full(self):
    free_gb = self.size_gb - self.used_size_gb
    free_perc = math.floor((free_gb / self.size_gb) * 100)

    if free_perc < FREE_LIMIT_PERCENT:
      print('DEBUG: ACTION="Low disk" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}" FREE_GB={3} FREE_%={4}'
            .format(self.get_label(), self.name, self.mount_point, free_gb, free_perc))
      return True
    else:
      return False

  def cal_new_size_gb(self):
    add_size_gb = math.ceil((RESIZE_PERCENT / 100) * self.size_gb)
    new_size_gb = self.size_gb + add_size_gb

    print('DEBUG: ACTION="New disk size" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}" ADD_GB={3} NEW_SIZE_GB%={4}'
          .format(self.get_label(), self.name, self.mount_point, add_size_gb, new_size_gb))
    return new_size_gb