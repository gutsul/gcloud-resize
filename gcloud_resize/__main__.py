from gcloud_resize import rest
from gcloud_resize.utils import is_root

if not is_root():
  exit("\nOnly root can run this script\n")

from gcloud_resize.logger import debug


# def resize(ZONE, disk):
#   add_gb = disk.increase_on(RESIZE_PERCENT)
#   new_size_gb = disk.size + add_gb
#   api.resize_disk(name=disk.name, size_gb=new_size_gb, zone=ZONE)
#
#   msg = 'DEBUG ACTION="Resize disk." NAME="{}" ADD_GB={} NEW_SIZE_GB={}' \
#       .format(disk.name, add_gb, new_size_gb)
#   log(msg)


# def apply(disk):
#   if disk.fstype == EXT4:
#     shell.resize_ext4_disk(label=disk.get_label())
#   elif disk.fstype == XFS:
#     shell.resize_xfs_disk(label=disk.get_label())
#   else:
#     msg = 'ERROR ACTION="Apply disk." NAME="{}" SOURCE="/dev/{}" FSTYPE="{}" REASON="Not supported file system."' \
#         .format(disk.name, disk.get_label(), disk.fstype)
#     log(msg)
#
#   msg = 'DEBUG ACTION="Apply disk." NAME="{}" SOURCE="/dev/{}" FSTYPE="{}"' \
#       .format(disk.name, disk.get_label(), disk.fstype)
#   log(msg)


def main():
  debug("Run")

  instance = rest.InstanceDetails()

  instance.disks

  # for disk in disks:
  #   if disk.boot is False:
  #     init(disk)
  #
  #     if disk.is_low():
  #       resize(ZONE, disk)
  #       apply(disk)
  #       init(disk)
  #       jarvis.say(instance=INSTANCE, environment=ENVIRONMENT, disk=disk)


# if __name__ == '__main__':
#   main()

