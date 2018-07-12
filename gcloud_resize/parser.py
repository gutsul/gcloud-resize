import re

from .models import Disk


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


def disk_info(line):
  regex = re.compile("[\w\/%]+")
  list = regex.findall(line)

  info = {
    "source": list[0],
    "fstype": list[1],
    "size_gb": list[2],
    "used_gb": list[3],
    "avail_gb": list[4],
    "pcent": list[5],
    "target": list[6]
  }

  return info


def environment(json):
  try:
    environment = json["labels"]["environment"]
  except:
    environment = "Unknown"
  return environment


def attached_disks(json):
  disks = []

  for item in json["disks"]:
    name = item["deviceName"]
    index = item["index"]
    boot = item["boot"]

    disk = Disk(name=name, index=index, boot=boot)
    disks.append(disk)

  return disks