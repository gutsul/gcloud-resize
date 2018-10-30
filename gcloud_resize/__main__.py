import argparse


def default(args):
  from gcloud_resize import rest, integrations
  from gcloud_resize.logger import info, debug

  instance_name = rest.get_instance_name()
  zone = rest.get_instance_zone()
  instance = rest.get_instance_details(name=instance_name, zone=zone)
  slack = integrations.Slack(instance=instance)

  info("Instance '{}' [{}]: Run on '{}' environment.".format(instance.name, instance.zone, instance.environment))

  for disk in instance.disks:

    if not disk.boot:
      debug("Disk '{}' [{}]: Disk is not boot.".format(disk.name, disk.device))

      if disk.low():
        info("Disk '{}' [{}]: A disk has a low space. ".format(disk.name, disk.device))

        new_size_gb = disk.calculate_size()
        rest.resize_disk(disk=disk, size_gb=new_size_gb)
        disk.apply_changes()

        slack.post(disk)
    else:
      debug("Disk '{}' [{}]: Disk is boot. Nothing to do.".format(disk.name, disk.device))


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