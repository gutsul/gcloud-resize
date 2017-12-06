import json

import requests

from settings import SLACK_URL


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