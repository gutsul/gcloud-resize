#!/usr/bin/env python3

import api
import utils

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

      if disk.is_low():

        msg = 'DEBUG: ACTION="Low disk" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}"'\
          .format(disk.get_label(), disk.name, disk.mount_point)
        utils.log(msg)

        api.resize_disk(disk, zone=ZONE)
        utils.apply_disk_changes(disk)

if __name__ == '__main__':
  main()
