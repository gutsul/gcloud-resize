from os import getuid

GIGABYTE = float(1 << 30)

def is_root():
  if getuid() == 0:
    return True
  else:
    return False


def to_GB(bytes):
  return round(bytes/GIGABYTE, 2)