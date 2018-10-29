from os import getuid


def is_root():
  if getuid() == 0:
    return True
  else:
    return False


def to_GB(bytes):
  GIGABYTE = float(1 << 30)
  return round(bytes/GIGABYTE, 2)