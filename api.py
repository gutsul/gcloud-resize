import utils
import requests
import time

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
