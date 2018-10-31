import json
import requests

from gcloud_resize import config
from gcloud_resize.logger import info, error

slack = config.SlackConfig()


class Slack(object):

  def __init__(self, instance):
    self._name = instance.name
    self._environment = instance.environment

  def _add_users(self):
    users_list = ""

    if slack.users:
      for user in slack.users:
        users_list += "<@{}> ".format(user)

    return users_list

  def post(self, disk_name, new_size_gb, old_size_gb):
    title = "Disk resize"
    users = self._add_users()

    message = "Disk *{name}* increased to _{new_size}GB_ _( ~{old_size}GB~ )_."\
      .format(name=disk_name, new_size=new_size_gb, old_size=old_size_gb)

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

    if slack.webhook:
      r = requests.post(slack.webhook, data=json.dumps(payload))

      if r.status_code == 200:
        info("Slack message send successfully.")
      else:
        error("{status} Can't send message to Slack.".format(r.status_code))
