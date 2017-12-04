#!/usr/bin/env python3

import api
import utils

BOOT_DISK = "sda"


def main():
  INSTANCE_NAME = api.get_instance_name()
  ZONE = api.get_geo_zone()
  disks = api.get_attached_disks()

  output = utils.get_blocked_device()

  for line in output.splitlines():
    label, size, mountpoint = utils.parse_device_info(line)

    disk = disks.get(label)

    if disk is not None:
      disk.mount_point = mountpoint
      disk.size_gb = utils.convert_to_gb(size)
      disk.used_size_gb = utils.get_size_gb(start_path=mountpoint)

  for label in disks.keys():
    disk = disks.get(label)

    if label != BOOT_DISK:

      print('DEBUG: ACTION="Checking disk" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}" SIZE_GB={3} USED_GB={}'
            .format(label, disk.name, disk.mount_point, disk.size_gb, disk.used_size_gb))

      if disk.is_full():
        api.resize_disk(disk, zone=ZONE)
        utils.apply_disk_changes(disk)

if __name__ == '__main__':
  main()




