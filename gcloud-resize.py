#!/usr/bin/env python3

from src import api, parser, shell
from src import utils


def main():

  INSTANCE_NAME = api.get_instance_name()
  msg = 'DEBUG: ACTION="Get instance name" INSTANCE="{0}"'.format(INSTANCE_NAME)
  utils.log(msg)


  ZONE = api.get_geo_zone()
  msg = 'DEBUG: ACTION="Get geo zone" ZONE="{0}"'.format(ZONE)
  utils.log(msg)


  disks = api.get_attached_disks()
  set_mount_points(disks)

  check_disks(ZONE, disks)


def check_disks(ZONE, disks):
  BOOT_DISK = "sda"

  for label in disks.keys():
    disk = disks.get(label)

    if label != BOOT_DISK:

      if disk.is_low():
        msg = 'DEBUG: ACTION="Low disk" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}"' \
          .format(disk.get_label(), disk.name, disk.mount_point)
        utils.log(msg)

        api.resize_disk(disk, zone=ZONE)
        shell.apply_disk_changes(disk)


def set_mount_points(disks):
  output = shell.get_blocked_device()

  for line in output.splitlines():
    label, mountpoint = parser.parse_device_info(line)

    disk = disks.get(label)

    if disk is not None:
      disk.mount_point = mountpoint


if __name__ == '__main__':
  main()
