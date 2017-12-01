#!/usr/bin/env python3
import math

import api
import utils


def need_resize(disk):
  free_mb = disk.size_mb - disk.used_size_mb
  free_perc = math.floor((free_mb / disk.size_mb ) * 100)

  print("Free MB: {0}".format(free_mb))
  print("Free %: {0}".format(free_perc))


def main():
  INSTANCE_NAME = api.get_instance_name()
  ZONE = api.get_geo_zone()
  disks = api.get_attached_disks()

  print("Instance Name: {0}".format(INSTANCE_NAME))
  print("Zone: {0}".format(ZONE))

  output = utils.get_blocked_device()

  for line in output.splitlines():
    label, size, mountpoint = utils.parse_device_info(line)

    disk = disks.get(label)

    if disk is not None:
      disk.mount_point = mountpoint
      disk.size_mb = utils.convert_to_mb(size)
      disk.used_size_mb = utils.get_size_mb(start_path=mountpoint)

  for label in disks.keys():
    disk = disks.get(label)

    print("-----------")
    print("Label: {0}".format(label))
    print("Name: {0}".format(disk.name))
    print("Mountpoint: {0}".format(disk.mount_point))
    print("Size MB: {0}".format(disk.size_mb))
    print("Used Size MB: {0}".format(disk.used_size_mb))

    need_resize(disk)


if __name__ == '__main__':
  main()



