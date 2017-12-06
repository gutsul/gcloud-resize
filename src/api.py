import time

import requests
from googleapiclient import discovery

from settings import PROJECT_ID
from src import utils, parser

service = discovery.build('compute', 'v1')

root_url = 'http://metadata.google.internal/computeMetadata/v1/instance/'
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}


def get_instance_name():
  url = root_url + "name"

  resp = requests.get(url, headers=METADATA_HEADERS)

  if resp.status_code == 503:
    time.sleep(1)
    get_instance_name()

  name = resp.text
  return name


def get_geo_zone():
  url = root_url + "zone"

  resp = requests.get(url, headers=METADATA_HEADERS)

  if resp.status_code == 503:
    time.sleep(1)
    get_geo_zone()

  # TODO: Perhaps need to move
  geo_zone = parser.parse_geo_zone(resp.text)

  return geo_zone


def get_attached_disks():
  url = root_url + "disks/?recursive=true"

  resp = requests.get(url, headers=METADATA_HEADERS)

  if resp.status_code == 503:
    time.sleep(1)
    get_attached_disks()

  # TODO: Perhaps need to move
  disks = parser.parse_disks(json=resp.json())
  return disks


def resize_disk(disk, zone):
  new_size = disk.cal_new_size_gb()
  name = disk.name

  disks_resize_request_body = {
    "sizeGb": new_size
  }

  request = service.disks().resize(project=PROJECT_ID, zone=zone, disk=name, body=disks_resize_request_body)
  response = request.execute()

  result = wait_for_operation(service, project=PROJECT_ID, zone=zone, operation=response['name'])

  print('DEBUG: ACTION="GCloud resize" NAME="{0}" NEW_SIZE={1} RESPONSE="{2}"'
        .format(name, new_size, result))


def wait_for_operation(compute, project, zone, operation):
    while True:
      result = compute.zoneOperations().get(
        project=project,
        zone=zone,
        operation=operation).execute()

      status = result['status']

      msg = 'DEBUG: ACTION="wait resize" STATUS="{0}"'.format(status)
      utils.log(msg)

      if status == 'DONE':
        if 'error' in result:
          raise Exception(result['error'])
        return result

      time.sleep(1)