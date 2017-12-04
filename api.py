from pprint import pprint

from googleapiclient import discovery

import utils
import requests
import time

PROJECT_ID = 'adlithium-1289'
service = discovery.build('compute', 'v1')

root_url = 'http://metadata.google.internal/computeMetadata/v1/instance/'
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}


def get_instance_name():
  url = root_url + "name"

  resp = requests.get(url, headers=METADATA_HEADERS)

  if resp.status_code == 503:
    time.sleep(1)
    get_instance_name()

  return resp.text


def get_geo_zone():
  url = root_url + "zone"

  resp = requests.get(url, headers=METADATA_HEADERS)

  if resp.status_code == 503:
    time.sleep(1)
    get_geo_zone()

  result = utils.parse_geo_zone(resp.text)

  return result


def get_attached_disks():
  url = root_url + "disks/?recursive=true"

  resp = requests.get(url, headers=METADATA_HEADERS)

  if resp.status_code == 503:
    time.sleep(1)
    get_attached_disks()

  disks = utils.parse_disks(json=resp.json())
  return disks


def resize_disk(disk, zone):
  new_size = disk.cal_new_size_gb()
  name = disk.name

  disks_resize_request_body = {
    "sizeGb": new_size
  }

  request = service.disks().resize(project=PROJECT_ID, zone=zone, disk=name, body=disks_resize_request_body)
  response = request.execute()

  pprint(response)

