import configparser
import re

from . import conf_dir, name

config_path = "{0}/{1}.conf".format(conf_dir, name)

config = configparser.ConfigParser()
config.read(config_path)


class Config(object):

  def __init__(self):
    self._config = config

  def get_property(self, section, name):
    if section not in self._config:
      print("Config section '{}' doesn't exist.".format(section))
      exit(1)
    else:
      if name not in self._config[section]:
        print("In config section '{0} property '{1}' doesn't exist.".format(section, name))
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
      print("ProjectId value cannot be empty.")
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
        print("FreeLimitPercent value must be a number in diapazone 0-99")
        exit(1)
      else:
        self._free_limit_percent = int(value)

    except ValueError:
      print("FreeLimitPercent value mast be a number")
      exit(1)

  @property
  def resize_percent(self):
    return self._resize_percent

  @resize_percent.setter
  def resize_percent(self, value):
    try:
      if int(value) < 0:
        print("ResizePercent value must be greater than zero")
        exit(1)
      else:
        self._resize_percent = int(value)

    except ValueError:
      print("ResizePercent value mast be a number")
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
      print("Slack webhook not valid.")
      exit(1)

    self._webhook = value

  @property
  def users(self):
    return self._users

  @users.setter
  def users(self, value):
    self._users = str(value).split(sep=",")