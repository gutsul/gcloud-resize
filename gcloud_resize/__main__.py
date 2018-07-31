from gcloud_resize.utils import is_root

if not is_root():
  exit("\nOnly root can run this script\n")

from gcloud_resize import rest, integrations
from gcloud_resize.logger import info, debug


def main():
  instance = rest.InstanceDetails()
  slack = integrations.Slack(instance=instance)

  info("Instance '{}' [{}]: Run on '{}' environment.".format(instance.name, instance.zone, instance.environment))

  for disk in instance.disks:

    if not disk.boot:
      debug("Disk '{}' [{}]: Disk is not boot.".format(disk.name, disk.label))

      if disk.low():
        info("Disk '{}' [{}]: A disk has a low space. ".format(disk.name, disk.label))
        response = instance.send_request_to_resize(disk)
        instance.apply_changes(disk)
        slack.post(disk)
    else:
      debug("Disk '{}' [{}]: Disk is boot. Nothing to do.".format(disk.name, disk.label))