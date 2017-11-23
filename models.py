class Disk:
  name = None
  index = 0
  mount_point = None
  size_mb = 0
  used_size_mb = 0

  def __init__(self, name, index):
    self.name = name
    self.index = index

  def get_label(self):
    result = "sd" + chr(97 + self.index)
    return result