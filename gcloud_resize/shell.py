import subprocess
from logging import error


def run(cmd):
  stdout = None
  stderr = None

  try:
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
  except:
    error(stdout.decode("utf-8"))
    exit(1)


def resize_ext4(disk):
  cmd = "sudo resize2fs {0}".format(disk.device)
  run(cmd)


def resize_xfs(disk):
  cmd = "sudo xfs_growfs {0}".format(disk.device)
  run(cmd)

