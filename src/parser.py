import re

from src.models import Disk


def parse_device_info(line):
  regex = re.compile('NAME="([a-z\d]*)" MOUNTPOINT="([\w\/]*)"')
  search = regex.search(line)

  label = search.group(1)
  mountpoint = search.group(2)

  return label, mountpoint


def parse_geo_zone(line):
  regex = re.compile("\/zones\/([a-z|\D|\d]+)")
  search = regex.search(line)

  geo_zone = search.group(1)

  return geo_zone


def parse_disks(json):
  disks = {}

  for item in json:
    name = item["deviceName"]
    index = item["index"]

    disk = Disk(name=name, index=index)

    disks[disk.get_label()] = disk

  return disks