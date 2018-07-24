import re


def parse_device_info(line):
  regex = re.compile('NAME="([a-z\d]*)" MOUNTPOINT="([\w\/]*)"')
  search = regex.search(line)

  label = search.group(1)
  mountpoint = search.group(2)

  return label, mountpoint


