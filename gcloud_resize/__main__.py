from gcloud_resize.utils import is_root

if not is_root():
  exit("\nOnly root can run this script\n")

from gcloud_resize import rest
from gcloud_resize.logger import info, debug


def main():
  instance = rest.InstanceDetails()

  info("Instance '{}' [{}]: Run.".format(instance.name, instance.zone))

  for disk in instance.disks:

    if not disk.boot:
      debug("Disk '{}' [{}]: Disk is not boot.".format(disk.name, disk.label))

      if disk.low():
        info("Disk '{}' [{}]: A disk has a low space. ".format(disk.name, disk.label))
        # response = instance.send_request_to_resize(disk)
        # instance.apply_changes(disk)
    #     send message to slack

    else:
      debug("Disk '{}' [{}]: Disk is boot.".format(disk.name, disk.label))


# if __name__ == '__main__':
#   main()

