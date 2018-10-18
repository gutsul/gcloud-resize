from os import getuid

def no_dimen(line):
  return line[:-1]


def is_root():
  if getuid() == 0:
    return True
  else:
    return False