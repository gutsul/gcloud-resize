import math

from settings import FREE_LIMIT_PERCENT


class Disk:
  name = None
  index = 0
  boot = False
  fstype = None
  target = None

  size = 0
  used = 0
  avail = 0
  pcent = 0

  add_gb = 0

  def __init__(self, name, index, boot):
    self.name = name
    self.index = index
    self.boot = boot

  def get_label(self):
    result = "sd" + chr(97 + self.index)
    return result

  def is_low(self):
    free_percent = 100 - self.pcent

    if free_percent <= FREE_LIMIT_PERCENT:
      return True
    else:
      return False

  def increase_on(self, percent):
    total_gb = self.size
    self.add_gb = math.ceil((percent / 100) * total_gb)

    return self.add_gb