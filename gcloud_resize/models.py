from math import ceil

import psutil

from gcloud_resize import config

resize = config.ResizeConfig()


class Disk:

  def __init__(self, name, index, boot):
    self._name = name
    self._index = index
    self._boot = boot
    self._fstype = None
    self._mountpoint = None
    self._total = None
    self._used = None
    self._free = None
    self._percent = None

    partitions = psutil.disk_partitions()

    for partition in partitions:
      if self.device in partition:
        print(partition)
        self._fstype = partition.fstype
        self._mountpoint = partition.mountpoint


    if self._mountpoint is not None:
      disk = psutil.disk_usage(self._mountpoint)

      self._total = disk.total
      self._used = disk.used
      self._free = disk.free
      self._percent = disk.percent

  @property
  def name(self):
    return self._name

  @property
  def index(self):
    return self._index

  @property
  def boot(self):
    return self._boot

  @property
  def device(self):
    device_path = "/dev/sd{}".format(chr(97 + self._index))
    return device_path

  @property
  def fstype(self):
    return self._fstype

  @property
  def mountpoint(self):
    return self._mountpoint

  @property
  def total(self):
    return self._total

  @property
  def used(self):
    return self._used

  @property
  def free(self):
    return self._free

  @property
  def percent(self):
    return self._percent

  # TODO: bytes to GB
  def low(self):
    free_percent = 100 - self.pcent

    if free_percent <= resize.free_limit_percent:
      return True
    else:
      return False

  def increase_size(self):
    add_gb = ceil((resize.resize_percent / 100) * self.size)
    new_size_gb = self.size + add_gb
    return new_size_gb
