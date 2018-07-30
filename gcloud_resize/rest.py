import re
import time

import requests
from googleapiclient import discovery
from gcloud_resize import config, shell
from gcloud_resize.logger import error, info
from math import ceil

service = discovery.build('compute', 'v1')
gcloud = config.GCloudConfig()
resize = config.ResizeConfig()


class Disk:
  XFS = 'xfs'
  EXT4 = 'ext4'
  SUPPORTED_FSTYPES = [XFS, EXT4]

  def __init__(self, name, index, boot):
    self._name = name
    self._label = "sd" + chr(97 + index)
    self._boot = boot
    self._source = None
    self._fstype = None
    self._target = None
    self._size = 0
    self._used = 0
    self._avail = 0
    self._pcent = 0

    shell.init_disk(self)

  @property
  def name(self):
    return self._name

  @property
  def label(self):
    return self._label

  @property
  def boot(self):
    return self._boot

  @property
  def source(self):
    return self._source

  @source.setter
  def source(self, value):
    self._source = value

  @property
  def fstype(self):
    return self._fstype

  # TODO: Add fstype validation
  @fstype.setter
  def fstype(self, value):
    self._fstype = value

  @property
  def target(self):
    return self._target

  @target.setter
  def target(self, value):
    self._target = value

  @property
  def size(self):
    return self._size

  @size.setter
  def size(self, value):
    self._size = int(value[:-1])

  @property
  def used(self):
    return self._used

  @used.setter
  def used(self, value):
    self._used = int(value[:-1])

  @property
  def avail(self):
    return self._avail

  @avail.setter
  def avail(self, value):
    self._avail = int(value[:-1])

  @property
  def pcent(self):
    return self._pcent

  @pcent.setter
  def pcent(self, value):
    self._pcent = int(value[:-1])

  def low(self):
    free_percent = 100 - self.pcent

    if free_percent <= resize.free_limit_percent:
      return True
    else:
      return False

  def increase_size(self):
    add_gb = ceil((resize.resize_percent / 100) * self.size)
    new_size_gb = self.size + add_gb
    return new_size_gb


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

    if disk.fstype in disk.supported_fstypes:

      if disk.fstype == disk.EXT4:
        shell.resize_ext4(disk)
      elif disk.fstype == disk.XFS:
        shell.resize_xfs(disk)

      info("Disk '{}' [{}]: Changes have been applied successfully.".format(disk.name, disk.label))

    else:
      error("Disk '{}' [{}]: Can't apply changes. Not supported file system '{}'.".format(disk.name, disk.label, disk.fstype))

  def send_request_to_resize(self, disk):
    new_size_gb = disk.increase_size()

    disks_resize_request_body = {
      "sizeGb": new_size_gb
    }

    request = service.disks().resize(project=gcloud.project_id, zone=self.zone, disk=disk.name, body=disks_resize_request_body)
    response = request.execute()
    result = self._wait_for_operation(service, project=gcloud.project_id, zone=self.zone, operation=response['name'])

    info("Disk '{}' [{}]: Send request to resize disk from {}Gb to {}Gb. Response: {}".format(disk.name, disk.label, disk.size, new_size_gb, result))

  def _wait_for_operation(compute, project, zone, operation):
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