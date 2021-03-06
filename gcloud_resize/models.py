import math

import psutil

from gcloud_resize import config, shell
from gcloud_resize.logger import info, error
from gcloud_resize.utils import to_GB, GIGABYTE

resize = config.ResizeConfig()

RESIZE_MODE = resize.resize_mode

FREE_SIZE = resize.free_size
INCREASE_SIZE = resize.increase_size

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

    if RESIZE_MODE == resize.MODE_FIXED:
      if to_GB(self.free) <= FREE_SIZE:
        return True
      else:
        return False

    elif RESIZE_MODE == resize.MODE_PERCENT:
      if self.percent >= USAGE_PERCENT:
        return True
      else:
        return False
    else:
      error("Not supported resize mode: '{mode}'.".format(mode=RESIZE_MODE))
      exit(1)


  def apply_changes(self):
    # Supported file systems
    EXT4 = "ext4"
    XFS = "xfs"

    if self.fstype == EXT4:
      shell.resize_ext4(self)
    elif self.fstype == XFS:
      shell.resize_xfs(self)
    else:
      error("Can't apply changes for disk {name} ({device}). Not supported file system '{fstype}'."
        .format(name=self.name, device=self.device, fstype=self.fstype))
      exit(1)

    info("Changes have been applied successfully for disk {name} ({device})".format(name=self.name, device=self.device))

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
    add_bytes = 0

    if RESIZE_MODE == resize.MODE_FIXED:
      add_bytes = INCREASE_SIZE * GIGABYTE

    elif RESIZE_MODE == resize.MODE_PERCENT:
      add_bytes = (RESIZE_PERCENT / 100) * self._total

    new_total_bytes = self._total + round(add_bytes)
    new_total_gigabytes = to_GB(new_total_bytes)

    size_gb = math.ceil(new_total_gigabytes)

    return size_gb


class InstanceDetails(object):

  def __init__(self):
    self._name = None
    self._zone = None
    self._environment = None
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