import math

import psutil

from gcloud_resize import config, shell
from gcloud_resize.logger import info, error
from gcloud_resize.utils import to_GB

resize = config.ResizeConfig()

USAGE_PERCENT = resize.usage_percent
RESIZE_PERCENT = resize.resize_percent


class Disk:

  def __init__(self, name, zone, index, boot):
    self._name = name
    self._zone = zone
    self._index = index
    self._boot = boot
    self._fstype = None
    self._mountpoint = None
    self._total = None
    self._used = None
    self._free = None
    self._percent = None

    self.refresh()


  @property
  def name(self):
    return self._name

  @property
  def zone(self):
    return self._zone

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

  @name.setter
  def name(self, value):
    self._name = value

  def low(self):
    if self.percent >= USAGE_PERCENT:
      return True
    else:
      return False

  def apply_changes(self):
    # Supported file systems
    EXT4 = "ext4"
    XFS = "xfs"

    if self.fstype == EXT4:
      shell.resize_ext4(self)
      info("Disk '{}' [{}]: Changes have been applied successfully.".format(self.name, self.device))
    elif self.fstype == XFS:
      shell.resize_xfs(self)
      info("Disk '{}' [{}]: Changes have been applied successfully.".format(self.name, self.device))
    else:
      error("Disk '{}' [{}]: Can't apply changes. Not supported file system '{}'.".format(
        self.name, self.device, self.fstype))

  def refresh(self):
    partitions = psutil.disk_partitions()

    for partition in partitions:
      if self.device in partition:
        self._fstype = partition.fstype
        self._mountpoint = partition.mountpoint

    if self._mountpoint is not None:
      disk = psutil.disk_usage(self._mountpoint)

      self._total = disk.total
      self._used = disk.used
      self._free = disk.free
      self._percent = disk.percent

  def calculate_size(self):
    add_bytes = (RESIZE_PERCENT / 100) * self._total

    new_total_bytes = self._total + round(add_bytes)
    new_total_gigabytes = to_GB(new_total_bytes)

    size_gb = math.ceil(new_total_gigabytes)

    return size_gb


class InstanceDetails(object):

  def __init__(self):
    self._name = None
    self._zone = None
    self._environment = "Unknown"
    self._disks = []

  @property
  def name(self):
    return self._name

  @property
  def zone(self):
    return self._zone

  @property
  def environment(self):
    return self._environment

  @property
  def disks(self):
    return self._disks

  @name.setter
  def name(self, value):
    self._name = value

  @zone.setter
  def zone(self, value):
    self._zone = value

  @environment.setter
  def environment(self, value):
    self._environment = value

  @disks.setter
  def disks(self, value):
    self._disks = value