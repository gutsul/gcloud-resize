import subprocess

# TODO: Remove loging
from src.utils import log


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


def resize_disk(label):
  cmd = "sudo resize2fs /dev/{0}".format(label)
  run(cmd)


def get_block_devices():
  cmd = "lsblk --output name,mountpoint --pairs --bytes"
  result = run(cmd)

  return result