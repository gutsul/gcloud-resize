import re
import time

import requests
from googleapiclient import discovery
from gcloud_resize import config, shell
from gcloud_resize.logger import error, info, debug

service = discovery.build('compute', 'v1')
gcloud = config.GCloudConfig()



class InstanceDetails(object):
  _root_url = 'http://metadata.google.internal/computeMetadata/v1/instance/'
  _metadata_headers = {'Metadata-Flavor': 'Google'}

  def __init__(self):
    self._name = self._get_name()
    self._zone = self._get_zone()
    self._json = self._get_json_info(name=self._name, zone=self._zone)
    self._environment = self._get_environment(json=self._json)
    self._disks = self._get_attached_disks(json=self._json)

  @property
  def name(self):
    return self._name

  @property
  def zone(self):
    return self._zone

  @property
  def environment(self):
    return self._environment

  @property
  def disks(self):
    return self._disks

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
    zone = regex.search(resp.text).group()

    return zone

  # TODO: Add try/accept and error msg.
  def _get_json_info(self, zone, name):
    request = service.instances().get(project=gcloud.project_id, zone=zone, instance=name)
    response = request.execute()
    debug("get_json_info: {}".format(response))
    return response

  def _get_environment(self, json):
    try:
      environment = json["labels"]["environment"]
    except:
      environment = "Unknown"
    return environment

  def _get_attached_disks(self, json):
    disks = []

    for item in json["disks"]:
      name = item["deviceName"]
      index = item["index"]
      boot = item["boot"]

      disk = Disk(name=name, index=index, boot=boot)
      disks.append(disk)

    return disks

  def apply_changes(self, disk):

    if disk.fstype in disk.SUPPORTED_FSTYPES:

      if disk.fstype == disk.EXT4:
        shell.resize_ext4(disk)
      elif disk.fstype == disk.XFS:
        shell.resize_xfs(disk)

      info("Disk '{}' [{}]: Changes have been applied successfully.".format(disk.name, disk.device))

    else:
      error("Disk '{}' [{}]: Can't apply changes. Not supported file system '{}'.".format(disk.name, disk.device, disk.fstype))

  def send_request_to_resize(self, disk):
    new_size_gb = disk.increase_size()

    disks_resize_request_body = {
      "sizeGb": new_size_gb
    }

    request = service.disks().resize(project=gcloud.project_id, zone=self.zone, disk=disk.name, body=disks_resize_request_body)
    response = request.execute()
    result = self._wait_for_operation(service, project=gcloud.project_id, zone=self.zone, operation=response['name'])

    info("Disk '{}' [{}]: Send request to resize disk from {}Gb to {}Gb. Response: {}".format(disk.name, disk.device, disk.size, new_size_gb, result))

  def _wait_for_operation(self, compute, project, zone, operation):
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