import re
import subprocess

from gcloud_resize.logger import info


def run(cmd):
  output = None

  try:
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()

    output = output.decode("utf-8")
    error = error.decode("utf-8")

  except:
    msg = 'ERROR  CMD="{0}"'.format(cmd)
    # log(msg)

  return output


def resize_ext4(disk):
  cmd = "sudo resize2fs /dev/{0}".format(disk.device)
  run(cmd)


def resize_xfs(disk):
  cmd = "sudo xfs_growfs /dev/{0}".format(disk.device)
  run(cmd)


def init_disk(disk):
  cmd = "sudo df -BG --output=source,fstype,size,used,avail,pcent,target /dev/{0}".format(disk.device)

  output = run(cmd)
  result = output.split("\n")[1]

  regex = re.compile("[\w\/%]+")
  list = regex.findall(result)

  disk.source = list[0]
  disk.fstype = list[1]
  disk.size = list[2]
  disk.used = list[3]
  disk.avail = list[4]
  disk.pcent = list[5]
  disk.target = list[6]

  msg = 'Initialized disk {}: name={} boot={} source={} target={} fstype={}\n size={}Gb used={}Gb used={}% avail={}Gb' \
       .format(disk.device, disk.name, disk.boot, disk.source, disk.target, disk.fstype, disk.size, disk.used, disk.pcent, disk.avail)

  info(msg)
