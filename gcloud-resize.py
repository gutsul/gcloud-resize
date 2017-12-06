#!/usr/bin/env python3
import math

from settings import RESIZE_PERCENT
from src import api, parser, shell, utils


def main():

  INSTANCE_NAME = api.get_instance_name()
  msg = 'DEBUG: ACTION="Get instance name" INSTANCE="{0}"'.format(INSTANCE_NAME)
  utils.log(msg)


  ZONE = api.get_geo_zone()
  msg = 'DEBUG: ACTION="Get geo zone" ZONE="{0}"'.format(ZONE)
  utils.log(msg)


  disks = api.get_attached_disks()
  analyze(disks)

  check_disks(ZONE, disks)


def check_disks(ZONE, disks):
  BOOT_DISK = "sda"

  for label in disks.keys():
    disk = disks.get(label)

    if label != BOOT_DISK:
      if disk.is_low():

        total_gb = math.ceil(utils.to_gb(disk.total))
        used_gb = math.ceil(utils.to_gb(disk.used))
        free_gb = math.ceil(utils.to_gb(disk.free))
        free_percent = 100 - disk.percent

        msg = 'DEBUG: ACTION="Low disk" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}" TOTAL_GB={3} USED_GB={4} FREE_GB={5} FREE_%={6}' \
          .format(disk.get_label(), disk.name, disk.mount_point, total_gb, used_gb, free_gb, free_percent)
        utils.log(msg)

        resize_disk(ZONE, disk)


def resize_disk(ZONE, disk):
  size_gb = disk.increase_on(RESIZE_PERCENT)
  api.resize_disk(name=disk.name, size_gb=size_gb, zone=ZONE)
  shell.resize_disk(label=disk.get_label())


def analyze(disks):
  EMPTY = ""

  output = shell.get_block_devices()

  for line in output.splitlines():
    label, mount_point = parser.parse_device_info(line)

    disk = disks.get(label)

    if disk is not None:
      if (mount_point != EMPTY):
        usage = utils.disk_usage(mount_point)

        disk.mount_point = mount_point
        disk.total = usage.total
        disk.used = usage.used
        disk.free = usage.free
        disk.percent = usage.percent

        msg = 'DEBUG ACTION="Analyze disk" LABEL="{0}" NAME="{1}" MOUNTPOINT="{2}" TOTAL={3} USED={4} USED_%={5} FREE={6}' \
          .format(disk.get_label(), disk.name, disk.mount_point, disk.total, disk.used, disk.percent, disk.free)
        utils.log(msg)


if __name__ == '__main__':
  main()
