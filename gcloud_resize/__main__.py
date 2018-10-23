from gcloud_resize.utils import is_root

if not is_root():
  exit("\nOnly root can run this script\n")

from gcloud_resize import rest, integrations
from gcloud_resize.logger import info, debug


def main():
  instance_name = rest.get_instance_name()
  zone = rest.get_instance_zone()

  instance = rest.get_instance_details(name=instance_name,
                                       zone=zone)
  slack = integrations.Slack(instance=instance)

  info("Instance '{}' [{}]: Run on '{}' environment.".format(instance.name, instance.zone, instance.environment))

  for disk in instance.disks:

    if not disk.boot:
      debug("Disk '{}' [{}]: Disk is not boot.".format(disk.name, disk.device))

      if disk.low():
        info("Disk '{}' [{}]: A disk has a low space. ".format(disk.name, disk.device))

        new_size = disk.calculate_size()
        rest.resize_disk(disk=disk, size=new_size)
        disk.apply_changes()

        slack.post(disk)
    else:
      debug("Disk '{}' [{}]: Disk is boot. Nothing to do.".format(disk.name, disk.device))
