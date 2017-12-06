import json
import re
import subprocess
import syslog

import requests

from settings import SLACK_URL
from src.models import Disk


def parse_geo_zone(line):
  regex = re.compile("\/zones\/([a-z|\D|\d]+)")
  search = regex.search(line)
  result = search.group(1)
  return result


def parse_disks(json):
  disks = {}

  for item in json:
    name = item["deviceName"]
    index = item["index"]

    disk = Disk(name=name, index=index)

    disks[disk.get_label()] = disk

  return disks


def shell(cmd):
  output = None

  try:
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()

    output = output.decode("utf-8")
    error = error.decode("utf-8")

    msg = 'DEBUG: ACTION="Run shell" COMMAND="{0}" OUT="{1}" ERR="{2}"'\
          .format(cmd, output, error)
    log(msg)
  except:
    msg = "Cannot run command: {0}".format(cmd)
    log(msg)

  return output


def apply_disk_changes(disk):
  label = disk.get_label()
  cmd = "sudo resize2fs /dev/{0}".format(label)
  shell(cmd)


def get_blocked_device():
  cmd = "lsblk --output name,mountpoint --pairs --bytes"
  result = shell(cmd)

  return result


def parse_device_info(line):
  regex = re.compile('NAME="([a-z\d]*)" MOUNTPOINT="([\w\/]*)"')
  search = regex.search(line)

  label = search.group(1)
  mountpoint = search.group(2)

  return label, mountpoint


def to_gb(bytes):
  BYTES_IN_MEGABYTE = 1048576
  BYTES_IN_GIGABYTE = BYTES_IN_MEGABYTE * 1000
  # BYTES_IN_GIGABYTE = 1073741824

  return int(bytes) / BYTES_IN_GIGABYTE


def log(message):
  syslog.syslog(syslog.LOG_DEBUG, message)


def jarvis_say():
  payload = {
  "attachments": [
    {
      "color": "good",
      "title": "Test message",
      "title_link": "link",
      "pretext": "<@ygrigortsevich> <@victordementiev> <@alexander>",
      "text": "Added *10 GB* to disk *postgres-data-3* (_now used: 68.5 %_)",
      "mrkdwn_in": [
        "text"
      ],
      "fields": [
		    {
          "title": "Instance",
          "value": "front-us-east",
          "short": "True"
        },
        {
          "title": "Environment",
          "value": "Production",
          "short": "True"
        }
      ]
    }
  ]
  }

  r = requests.post(SLACK_URL, data=json.dumps(payload))
  print(r.text)
  print(r.status_code)
