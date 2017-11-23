#!/usr/bin/env python3
import api

# lsblk -o name,size,MOUNTPOINT -P
# ls -l /dev/disk/by-id/google-*

# sudo resize2fs /dev/[DISK_ID]


def main():
  INSTANCE_NAME = api.get_instance_name()
  ZONE = api.get_geo_zone()
  disks = api.get_attached_disks()

  print("Instance Name: {0}".format(INSTANCE_NAME))
  print("Zone: {0}".format(ZONE))
  print("Disks:")

  for disk in disks:
    print("Name: {0}".format(disk.name))
    print("Label: {0}".format(disk.get_label()))

if __name__ == '__main__':
  main()
