#!/usr/bin/env python3
from src import api, utils

BOOT_DISK = "sda"


def main():
  INSTANCE_NAME = api.get_instance_name()
  ZONE = api.get_geo_zone()
  disks = api.get_attached_disks()

  output = utils.get_blocked_device()

  # Set mountpoints
  for line in output.splitlines():
    label, mountpoint = utils.parse_device_info(line)

    disk = disks.get(label)

    if disk is not None:
      disk.mount_point = mountpoint

  # check disks
  for label in disks.keys():
    disk = disks.get(label)

    if label != BOOT_DISK:
      usage = disk.usage()

      print("usage total: {0}".format(usage.total))
      print("usage used: {0}".format(usage.used))

      total_gb = utils.to_gb(usage.total)
      used_gb = utils.to_gb(usage.used)
      print('DEBUG: ACTION="Checking disk" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}" TOTAL_GB={3} USED_GB={4}'
            .format(label, disk.name, disk.mount_point, total_gb, used_gb))

      if disk.is_low():
        api.resize_disk(disk, zone=ZONE)
        utils.apply_disk_changes(disk)

if __name__ == '__main__':
    main()



