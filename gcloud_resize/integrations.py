import json
import requests

from gcloud_resize import config
from gcloud_resize.logger import info, error

slack = config.SlackConfig()


class Slack(object):

  def __init__(self, instance):
    self._name = instance.name
    self._environment = instance.environment

  def _format_users(self):
    users_list = ""
    for user in slack.users:
      users_list += "<@{}> ".format(user)
    return users_list

  def post(self, disk):
    title = "Disk resize"
    users = self._format_users()
    message = "Disk *{}* increased to _{}GB_ _( ~{}GB~ )_.".format(disk.name, disk.increase_size(), disk.size)

    payload = {
      "attachments": [
        {
          "color": "good",
          "title": title,
          "title_link": "link",
          "pretext": users,
          "text": message,
          "mrkdwn_in": [
            "text"
          ],
          "fields": [
            {
              "title": "Instance",
              "value": self._name,
              "short": True
            },
            {
              "title": "Environment",
              "value": self._environment,
              "short": True
            }
          ]
        }
      ]
    }

    if slack.webhook != "":

      r = requests.post(slack.webhook, data=json.dumps(payload))

      if r.status_code == 200:
        info("Disk '{}' [{}]: Slack message send successfully.".format(disk.name, disk.label))
      else:
        error("Disk '{}' [{}]: Can't send message to SLACK. Response: {}".format(disk.name, disk.label, r.text))





