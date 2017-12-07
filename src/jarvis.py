import json

import requests

from settings import SLACK_URL
from src.utils import log


def say(instance, disk):
  title = "Test message"
  recepients = "<@ygrigortsevich> <@victordementiev> <@alexander>"
  message = "Added *10 GB* to disk *postgres-data-3* (_now used: 68.5 %_)"

  instance = "test-us-east"
  environment = "Test"

  payload = {
  "attachments": [
    {
      "color": "good",
      "title": title,
      "title_link": "link",
      "pretext": recepients,
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

  msg = 'DEBUG ACTION="JARVIS Say" CODE={0} STATUS="{1}"'.format(r.status_code, r.text)
  log(message=msg)
