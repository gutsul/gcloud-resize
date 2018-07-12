import configparser

config = configparser.ConfigParser
config.read("conf/gcloud-resize.conf")


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
  section = "GCloud Settings"

  @property
  def project_id(self):
    return self.get_property(section=self.section, name="ProjectId")


class ResizeConfig(Config):
  section = "Resize Settings"

  @property
  def free_limit_percent(self):
    return self.get_property(section=self.section, name="FreeLimitPercent")

  @property
  def resize_percent(self):
    return self.get_property(section=self.section, name="ResizePercent")


class SlackConfig(Config):
  section = "Slack Settings"

  @property
  def webhook(self):
    return self.get_property(section=self.section, name="SlackWebhook")

  @property
  def users(self):
    return self.get_property(section=self.section, name="SlackUsers")