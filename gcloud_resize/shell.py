import subprocess


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

