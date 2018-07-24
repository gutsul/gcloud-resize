import re
import time

import requests
from googleapiclient import discovery
from gcloud_resize import config
from gcloud_resize.logger import error
from math import ceil

service = discovery.build('compute', 'v1')
gcloud = config.GCloudConfig()
resize = config.ResizeConfig()


class Disk:
  fstype = None
  target = None

  size = 0
  used = 0
  avail = 0
  pcent = 0

  add_gb = 0

  def __init__(self, name, index, boot):
    self._name = name
    self._label = "sd" + chr(97 + index)
    self._boot = boot

  @property
  def name(self):
    return self._name

  @property
  def label(self):
    return self._label

  @property
  def boot(self):
    return self._boot



  def is_low(self):
    free_percent = 100 - self.pcent

    if free_percent <= FREE_LIMIT_PERCENT:
      return True
    else:
      return False

  def increase_on(self, percent):
    total_gb = self.size
    self.add_gb = ceil((percent / 100) * total_gb)

    return self.add_gb


class InstanceDetails(object):
  _root_url = 'http://metadata.google.internal/computeMetadata/v1/instance/'
  _metadata_headers = {'Metadata-Flavor': 'Google'}

  def __init__(self):
    self._name = self._get_name()
    self._zone = self._get_zone()
    self._json = self._get_json_info()
    self._environment = self._get_environment()

  @property
  def name(self):
    return self._name

  @property
  def zone(self):
    return self._zone

  @property
  def environment(self):
    return self._environment

  def _get_name(self):
    url = self._root_url + "name"
    resp = requests.get(url=url, headers= self._metadata_headers)

    if resp.status_code != 200:
      error("Cannot get instance name. Response status code is {}".format(resp.status_code))
      exit(1)

    name = resp.text
    return name

  def _get_zone(self):
    url = self._root_url + "zone"
    resp = requests.get(url=url, headers=self._metadata_headers)

    if resp.status_code != 200:
      error("Cannot get instance zone. Response status code is {}".format(resp.status_code))
      exit(1)

    regex = re.compile("(?:\w|-)+$")
    zone = regex.search(resp.text)

    return zone

  # TODO: Add try/accept and error msg.
  def _get_json_info(self):
    request = service.instances().get(project=gcloud.project_id, zone=self.zone, instance=self.name)
    response = request.execute()
    return response

  def _get_environment(self):
    try:
      environment = self._json["labels"]["environment"]
    except:
      environment = "Unknown"
    return environment





def resize_disk(name, size_gb, zone):

  disks_resize_request_body = {
    "sizeGb": size_gb
  }

  request = service.disks().resize(project=PROJECT_ID, zone=zone, disk=name, body=disks_resize_request_body)
  response = request.execute()

  result = wait_for_operation(service, project=PROJECT_ID, zone=zone, operation=response['name'])

  msg = 'DEBUG ACTION="GCloud resize" NAME="{0}" NEW_SIZE={1} RESPONSE="{2}"'\
        .format(name, size_gb, result)


def wait_for_operation(compute, project, zone, operation):
    while True:
      result = compute.zoneOperations().get(
        project=project,
        zone=zone,
        operation=operation).execute()

      status = result['status']

      msg = 'DEBUG ACTION="wait resize" STATUS="{0}"'.format(status)


      if status == 'DONE':
        if 'error' in result:
          raise Exception(result['error'])
        return result

      time.sleep(1)