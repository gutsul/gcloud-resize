import re
import time

import requests
from googleapiclient import discovery
from gcloud_resize import config
from gcloud_resize.logger import error, info, debug
from gcloud_resize.models import Disk, InstanceDetails

gcloud = config.GCloudConfig()

service = discovery.build('compute', 'v1')

# TODO: add try/catch
def get_instance_name():
  url = "http://metadata.google.internal/computeMetadata/v1/instance/name"
  metadata_headers = {'Metadata-Flavor': 'Google'}

  resp = requests.get(url=url, headers=metadata_headers)

  if resp.status_code != 200:
    error("Cannot get instance name. Response status code is {}".format(resp.status_code))
    exit(1)

  name = resp.text

  return name

# TODO: add try/catch
def get_instance_zone():
  url = "http://metadata.google.internal/computeMetadata/v1/instance/zone"
  metadata_headers = {'Metadata-Flavor': 'Google'}

  resp = requests.get(url=url, headers=metadata_headers)

  if resp.status_code != 200:
    error("Cannot get instance zone. Response status code is {}".format(resp.status_code))
    exit(1)

  regex = re.compile("(?:\w|-)+$")
  zone = regex.search(resp.text).group()

  return zone


def _get_environment(json):
  try:
    environment = json["labels"]["environment"]
  except:
    environment = "Unknown"
  return environment


def _get_attached_disks(json, zone):
  disks = []

  for item in json["disks"]:
    name = item["deviceName"]
    index = item["index"]
    boot = item["boot"]

    disk = Disk(name=name, zone=zone, index=index, boot=boot)
    disks.append(disk)

  return disks


# TODO: Add try/accept and error msg.
def get_instance_details(name, zone):
  request = service.instances().get(project=gcloud.project_id, zone=zone, instance=name)
  response = request.execute()

  debug("get_instance_details: {}".format(response))

  instance = InstanceDetails()
  instance.name = name
  instance.zone = zone
  instance.environment = _get_environment(json=response)
  instance.disks = _get_attached_disks(json=response, zone=zone)

  return instance


def _wait_for_operation(compute, project, zone, operation):
  while True:
    result = compute.zoneOperations().get(
      project=project,
      zone=zone,
      operation=operation).execute()
    status = result['status']
    debug("Wait for operation from GCloud API. Response: {}".format(result))
    if status == 'DONE':
      if 'error' in result:
        raise Exception(result['error'])
      return result
    time.sleep(1)

# TODO Add try/catch
def resize_disk(disk, size_gb):

  disks_resize_request_body = {
    "sizeGb": size_gb
  }

  request = service.disks().resize(project=gcloud.project_id, zone=disk.zone, disk=disk.name, body=disks_resize_request_body)
  response = request.execute()
  result = _wait_for_operation(service, project=gcloud.project_id, zone=disk.zone, operation=response['name'])

  info("Disk '{}' [{}]: Send request to resize disk to {}Gb. Response: {}".format(disk.name, disk.device, size_gb, result))

