import re
import subprocess

from src.models import Disk


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


# TODO: Show error
def shell(cmd):
  output = None

  try:
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()

    output = output.decode("utf-8")
    error = error.decode("utf-8")

    print('DEBUG: ACTION="Run shell" COMMAND="{0}" OUT="{1}" ERR="{2}"'
          .format(cmd, output, error))

  except:
    print("Cannot run command: {0}".format(cmd))

  return output


def apply_disk_changes(disk):
  label = disk.get_label()
  cmd = "sudo resize2fs /dev/{0}".format(label)
  shell(cmd)


def get_blocked_device():
  cmd = "lsblk --output name,mountpoint --pairs --bytes"
  result = shell(cmd)

  return result


def parse_device_info(line):
  regex = re.compile('NAME="([a-z\d]*)" MOUNTPOINT="([\w\/]*)"')
  search = regex.search(line)

  label = search.group(1)
  mountpoint = search.group(2)

  return label, mountpoint


def to_gb(bytes):
  BYTES_IN_MEGABYTE = 1048576
  BYTES_IN_GIGABYTE = BYTES_IN_MEGABYTE * 1000
  # BYTES_IN_GIGABYTE = 1073741824

  return int(bytes) / BYTES_IN_GIGABYTE

