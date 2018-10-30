import argparse

from gcloud_resize.utils import to_GB


def default(args):
  from gcloud_resize import rest, integrations
  from gcloud_resize.logger import info, debug

  instance_name = rest.get_instance_name()
  zone = rest.get_instance_zone()
  instance = rest.get_instance_details(name=instance_name, zone=zone)
  slack = integrations.Slack(instance=instance)

  for disk in instance.disks:

    if not disk.boot:
      debug("Disk {name} (device) is not boot.".format(name=disk.name, device=disk.device))

      if disk.low():
        info("A disk {name} (device) has a low space. ".format(name=disk.name, device=disk.device))

        new_size_gb = disk.calculate_size()
        old_size_gb = to_GB(disk.total)

        rest.resize_disk(disk=disk, size_gb=new_size_gb)
        disk.apply_changes()

        slack.post(disk_name=disk.name, new_size_gb=new_size_gb, old_size_gb=old_size_gb)
    else:
      debug("Disk {name} (device) is boot. Nothing to do.".format(name=disk.name, device=disk.device))


def parse_args():
  from . import __version__
  description = "CLI tool that can resize persistent disks on Google Cloud Platform."

  parser = argparse.ArgumentParser(description=description)
  parser.set_defaults(func=default)

  parser.add_argument('-v', '--version', action='version',
                      version='%(prog)s {version}'.format(version=__version__))

  return parser.parse_args()


def main():
  args = parse_args()
  args.func(args)