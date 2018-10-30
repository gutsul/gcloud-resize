import json
import re
import time

import requests
from googleapiclient import discovery
from googleapiclient.errors import HttpError

from gcloud_resize import config
from gcloud_resize.logger import error, info
from gcloud_resize.models import Disk, InstanceDetails

gcloud = config.GCloudConfig()


def get_instance_name():
  url = "http://metadata.google.internal/computeMetadata/v1/instance/name"
  metadata_headers = {'Metadata-Flavor': 'Google'}

  resp = requests.get(url=url, headers=metadata_headers)

  if resp.status_code != 200:
    error("{status} Cannot get instance name.".format(status=resp.status_code))
    exit(1)

  name = resp.text
  return name


def get_instance_zone():
  url = "http://metadata.google.internal/computeMetadata/v1/instance/zone"
  metadata_headers = {'Metadata-Flavor': 'Google'}

  resp = requests.get(url=url, headers=metadata_headers)

  if resp.status_code != 200:
    error("{status} Cannot get instance zone.".format(status=resp.status_code))
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


def get_instance_details(name, zone):
  service = discovery.build('compute', 'v1')
  request = service.instances().get(project=gcloud.project_id, zone=zone, instance=name)
  instance = InstanceDetails()

  try:
    response = request.execute()

    instance.name = name
    instance.zone = zone
    instance.environment = _get_environment(json=response)
    instance.disks = _get_attached_disks(json=response, zone=zone)

  except HttpError as err:
    content = err.content.decode("utf-8")
    data = json.loads(content)

    status = data["error"]["code"]
    message = data["error"]["message"]

    if message == "Insufficient Permission":
      error("{} Virtual machine hasn`t read/write permissions for Compute Engine API.".format(status))
    else:
      error(err)
    exit(1)

  return instance


def _wait_for_operation(compute, project, zone, operation):
  while True:
    result = compute.zoneOperations().get(
      project=project,
      zone=zone,
      operation=operation).execute()

    if result['status'] == 'DONE':
      if 'error' in result:
        raise Exception(result['error'])
      return result

    time.sleep(1)


def resize_disk(disk, size_gb):
  info("Send request to resize disk {name} ({device}) to {size} GB."
       .format(name=disk.name, device=disk.device, size=size_gb))

  disks_resize_request_body = {
    "sizeGb": size_gb
  }

  service = discovery.build('compute', 'v1')
  request = service.disks().resize(project=gcloud.project_id, zone=disk.zone,
                                   disk=disk.name, body=disks_resize_request_body)
  try:
    response = request.execute()
    _wait_for_operation(service, project=gcloud.project_id, zone=disk.zone, operation=response['name'])
  except HttpError as err:
    error(err)
    exit(1)
