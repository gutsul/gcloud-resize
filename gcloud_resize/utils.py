from os import getuid


def is_root():
  if getuid() == 0:
    return True
  else:
    return False