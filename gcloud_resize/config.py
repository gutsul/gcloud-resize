import configparser
import re

from . import CONFIG_FILENAME
from .logger import error

config = configparser.ConfigParser()
config.read(CONFIG_FILENAME)


class Config(object):

  def __init__(self):
    self._config = config

  def get_property(self, section, name):
    if section not in self._config:
      error("Config section '{}' doesn't exist.".format(section))
      exit(1)
    else:
      if name not in self._config[section]:
        error("In config section '{0} property '{1}' doesn't exist.".format(section, name))
        exit(1)
      else:
        return self._config[section][name]


class GCloudConfig(Config):
  _section = "GCloud Settings"

  def __init__(self):
    Config.__init__(self)
    self.project_id = self.get_property(section=self._section, name="ProjectId")

  @property
  def project_id(self):
    return self._project_id

  @project_id.setter
  def project_id(self, value):
    # if value == "": raise ValueError("ProjectId value cannot be empty.")
    if value == "":
      error("ProjectId value cannot be empty.")
      exit(1)

    self._project_id = value


class ResizeConfig(Config):
  _section = "Resize Settings"

  def __init__(self):
    Config.__init__(self)
    self.free_limit_percent = self.get_property(section=self._section, name="FreeLimitPercent")
    self.resize_percent = self.get_property(section=self._section, name="ResizePercent")

  @property
  def free_limit_percent(self):
    return self._free_limit_percent

  @free_limit_percent.setter
  def free_limit_percent(self, value):
    try:
      if int(value) < 0 or int(value) >= 100:
        error("FreeLimitPercent value must be a number in diapazone 0-99")
        exit(1)
      else:
        self._free_limit_percent = int(value)

    except ValueError:
      error("FreeLimitPercent value mast be a number")
      exit(1)

  @property
  def resize_percent(self):
    return self._resize_percent

  @resize_percent.setter
  def resize_percent(self, value):
    try:
      if int(value) < 0:
        error("ResizePercent value must be greater than zero")
        exit(1)
      else:
        self._resize_percent = int(value)

    except ValueError:
      error("ResizePercent value mast be a number")
      exit(1)


class SlackConfig(Config):
  _section = "Slack Settings"

  def __init__(self):
    Config.__init__(self)
    self.webhook = self.get_property(section=self._section, name="SlackWebhook")
    self.users = self.get_property(section=self._section, name="SlackUsers")

  @property
  def webhook(self):
    return self._webhook

  @webhook.setter
  def webhook(self, value):
    regex = re.compile("^(?:http)s?:\/\/hooks.slack.com\/services\/[\d\w]{9}\/[\d\w]{9}\/[\d\w]{24}", re.IGNORECASE)
    webhook = re.match(regex, value)

    if webhook is None:
      error("Slack webhook not valid.")
      exit(1)

    self._webhook = value

  @property
  def users(self):
    return self._users

  @users.setter
  def users(self, value):
    self._users = str(value).split(sep=",")