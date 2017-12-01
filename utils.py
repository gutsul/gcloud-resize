import subprocess
import os
import re

from models import Disk


def parse_geo_zone(line):
  regex = re.compile("\/zones\/([a-z|\D|\d]+)")
  search = regex.search(line)
  result = search.group(1)
  return result


def parse_disks(json):
  disks = {}

  for item in json:
    name = item["deviceName"]
    index = item["index"]

    disk = Disk(name=name, index=index)

    disks[disk.get_label()] = disk

  return disks


def get_size_mb(start_path='.'):
  total_size = 0
  for dirpath, dirnames, filenames in os.walk(start_path):
    for f in filenames:
      fp = os.path.join(dirpath, f)
      total_size += os.path.getsize(fp)

  return convert_to_mb(total_size)


def shell(cmd):
  output = None

  try:
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()

    output = output.decode("utf-8")
    error = error.decode("utf-8")

  except:
    print("Cannot run command: {0}".format(cmd))

  return output


def apply_disk_changes(label):
  cmd = "sudo resize2fs /dev/{0}".format(label)
  shell(cmd)


def get_blocked_device():
  cmd = "lsblk --output name,size,mountpoint --pairs --bytes"
  result = shell(cmd)

  return result


def parse_device_info(line):
  regex = re.compile('NAME="([a-z\d]*)" SIZE="(\d*)" MOUNTPOINT="([a-z\/]*|[A-Z\[\]]*)"')
  search = regex.search(line)

  label = search.group(1)
  size = search.group(2)
  mountpoint = search.group(3)

  return label, size, mountpoint


def convert_to_mb(bytes):
  BYTES_IN_MEGABYTE = 1048576
  return int(bytes) / BYTES_IN_MEGABYTE





