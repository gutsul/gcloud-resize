import math

from settings import FREE_LIMIT_PERCENT
from src.utils import to_gb, log


class Disk:
  name = None
  index = 0
  mount_point = None

  total = 0
  used = 0
  free = 0
  percent = 0

  def __init__(self, name, index):
    self.name = name
    self.index = index

  def get_label(self):
    result = "sd" + chr(97 + self.index)
    return result

  def is_low(self):
    free_percent = 100 - self.percent

    if free_percent < FREE_LIMIT_PERCENT:
      return True
    else:
      return False

  def increase_on(self, percent):

    total_gb = math.ceil(to_gb(self.total))
    add_gb = math.ceil((percent / 100) * total_gb)
    new_size_gb = total_gb + add_gb

    return new_size_gb