import subprocess

from .utils import log


def run(cmd):
  output = None

  try:
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()

    output = output.decode("utf-8")
    error = error.decode("utf-8")

  except:
    msg = 'ERROR  CMD="{0}"'.format(cmd)
    log(msg)

  return output


def resize_ext4_disk(label):
  cmd = "sudo resize2fs /dev/{0}".format(label)
  run(cmd)


def resize_xfs_disk(label):
  cmd = "sudo xfs_growfs /dev/{0}".format(label)
  run(cmd)


def get_disk_info(label):
  cmd = "sudo df -BG --output=source,fstype,size,used,avail,pcent,target /dev/{0}".format(label)

  output = run(cmd)
  result = output.split("\n")[1]

  return result