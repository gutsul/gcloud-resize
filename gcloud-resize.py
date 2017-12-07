#!/usr/bin/env python3

from settings import RESIZE_PERCENT
from src import api, parser, shell, utils, jarvis
from src.utils import show

INSTANCE = api.get_instance_name()
ZONE = api.get_geo_zone()


def main():
  disks = api.get_attached_disks()
  analyze(disks)
  check_disks(disks)


def check_disks(disks):
  BOOT_DISK = "sda"

  for label in disks.keys():
    disk = disks.get(label)

    if label != BOOT_DISK:
      if disk.is_low():

        show(action="Disk Low", disk=disk)

        resize_disk(disk)
        jarvis.say(instance=INSTANCE, disk=disk)


def resize_disk(disk):
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
      if mount_point != EMPTY:
        usage = utils.disk_usage(mount_point)

        disk.mount_point = mount_point
        disk.total = usage.total
        disk.used = usage.used
        disk.free = usage.free
        disk.percent = usage.percent

        show(action="Analyze disk", disk=disk)


if __name__ == '__main__':
  main()
