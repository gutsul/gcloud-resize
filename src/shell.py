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

    msg = 'DEBUG: ACTION="Run shell" COMMAND="{0}" OUT="{1}" ERR="{2}"'\
          .format(cmd, output, error)
    log(msg)
  except:
    msg = "Cannot run command: {0}".format(cmd)
    log(msg)

  return output


def apply_disk_changes(disk):
  label = disk.get_label()
  cmd = "sudo resize2fs /dev/{0}".format(label)
  run(cmd)


def get_blocked_device():
  cmd = "lsblk --output name,mountpoint --pairs --bytes"
  result = run(cmd)

  return result