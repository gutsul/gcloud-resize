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

    print("Free GB: {0}".format(free_gb))
    print("Free %: {0}".format(free_perc))

    if free_perc < FREE_LIMIT_PERCENT:
      return True
    else:
      return False

  def cal_new_size_gb(self):
    add_size = math.ceil((RESIZE_PERCENT / 100) * self.size_gb)
    new_size_gb = self.size_gb + add_size

    print("Resize disk {0}: {1}".format(self.name, add_size))
    return new_size_gb