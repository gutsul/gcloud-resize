import json

import requests

from settings import SLACK_URL, SLACK_USERS
from src.utils import log


def say(instance, environment, disk):
  title = "Disk resize"
  message = "Added *{0} GB* to disk *{1}* (_now used: {2} %_)".format(disk.add_gb, disk.name, disk.percent)

  payload = {
  "attachments": [
    {
      "color": "good",
      "title": title,
      "title_link": "link",
      "pretext": SLACK_USERS,
      "text": message,
      "mrkdwn_in": [
        "text"
      ],
      "fields": [
		    {
          "title": "Instance",
          "value": instance,
          "short": "True"
        },
        {
          "title": "Environment",
          "value": environment,
          "short": "True"
        }
      ]
    }
  ]
  }

  r = requests.post(SLACK_URL, data=json.dumps(payload))

  msg = 'DEBUG ACTION="J.A.R.V.I.S Say" CODE={0} STATUS="{1}"'.format(r.status_code, r.text)
  log(message=msg)
