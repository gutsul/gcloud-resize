#!/usr/bin/env python3

from settings import RESIZE_PERCENT
from src import api, parser, shell, jarvis
from src.utils import no_dimen, log


def init(disk):
  label = disk.get_label
  line = shell.get_disk_info(label=label)

  info = parser.disk_info(line)

  source = info.get("source")

  fstype = info.get("fstype")
  disk.fstype = fstype

  size_gb = info.get("size_gb")
  disk.size = int(no_dimen(size_gb))

  used_gb = info.get("used_gb")
  disk.used = int(no_dimen(used_gb))

  avail_gb = info.get("avail_gb")
  disk.avail = int(no_dimen(avail_gb))

  pcent = info.get("pcent")
  disk.pcent = int(no_dimen(pcent))

  target = info.get("target")
  disk.target = int(no_dimen(target))

  msg = 'DEBUG ACTION="Init disk." NAME="{}" SOURCE="{}" FSTYPE="{}" SIZE_GB={} USED_GB={} USED_%={} AVAIL_GB={} TARGET={}' \
    .format(disk.name, source, disk.fstype, disk.size, disk.used, disk.pcent, disk.avail, disk.target)
  log(msg)


def main():
  INSTANCE = api.get_instance_name()
  ZONE = api.get_geo_zone()

  instance_json = api.get_instance(instance=INSTANCE, zone=ZONE)

  ENVIRONMENT = parser.environment(json=instance_json)

  disks = parser.attached_disks(json=instance_json)

  for disk in disks:
    if disk.boot is False:

      init(disk)

      if disk.is_low():
        add_gb = disk.increase_on(RESIZE_PERCENT)
        new_size_gb = disk.size + add_gb

        api.resize_disk(name=disk.name, size_gb=new_size_gb, zone=ZONE)

        if disk.fstype == 'ext4':
          shell.resize_ext4_disk(label=disk.get_label())
        elif disk.fstype == 'xfs':
          shell.resize_xfs_disk(label=disk.get_label)
        else:
          print("Cannot resize. Not supported file system.")

        jarvis.say(instance=INSTANCE, environment=ENVIRONMENT, disk=disk)

if __name__ == '__main__':
  main()
