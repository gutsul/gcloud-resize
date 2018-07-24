import re


def parse_device_info(line):
  regex = re.compile('NAME="([a-z\d]*)" MOUNTPOINT="([\w\/]*)"')
  search = regex.search(line)

  label = search.group(1)
  mountpoint = search.group(2)

  return label, mountpoint


# def disk_info(line):
#   regex = re.compile("[\w\/%]+")
#   list = regex.findall(line)
#
#   info = {
#     "source": list[0],
#     "fstype": list[1],
#     "size_gb": list[2],
#     "used_gb": list[3],
#     "avail_gb": list[4],
#     "pcent": list[5],
#     "target": list[6]
#   }
#
#   return info



