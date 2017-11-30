import os
import re

from models import Disk


def parse_geo_zone(line):
  regex = re.compile("\/zones\/([a-z|\D|\d]+)")
  search = regex.search(line)
  result = search.group(1)
  return result


def parse_disks(json):
  disks = []

  for item in json:
    name = item["deviceName"]
    index = item["index"]
    disks.append(Disk(name=name, index=index))

  return disks


def get_size_mb(start_path='.'):
  total_size = 0
  for dirpath, dirnames, filenames in os.walk(start_path):
    for f in filenames:
      fp = os.path.join(dirpath, f)
      total_size += os.path.getsize(fp)

  return total_size / 1000000
