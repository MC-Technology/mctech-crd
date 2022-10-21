import yaml


class ConfigReader:
  def __init__(self, config_path):
    self.config_path = config_path
    self.read_config()

  def keyboard_trigger(self):
    return self.cfg.get('keyboard_trigger', 0)

  def get_logging(self):
    return self.cfg['logging']

  def get_location(self):
    return self.cfg['location']

  def get_min_interval(self):
    try:
      return self.cfg['min_interval']
    except:
      return 0

  def set_location(self, location):
    self.cfg['location'] = location

  def has_media_player(self):
    try:
      return self.cfg['media_player']
    except:
      return False

  def network(self):
    try:
      return self.cfg['network']
    except:
      return {}

  def google_logging(self):
    try:
      return self.cfg['google_logging']
    except:
      return False

  def has_text_logging(self):
    try:
      return self.cfg['text_logging']
    except:
      return False

  def has_gps_sensor(self):
    try:
      return self.cfg['gps_sensor']
    except:
      return False

  def get_midi_controls(self):
    return self.cfg['midi_controls']

  def has_servo_motor(self):
    try:
      return self.cfg['servo_motor']
    except:
      return False

  def get_relay_output(self):
    try:
      return self.cfg['relay_output']
    except:
      return False

  def get_switch_input(self):
    try:
      return self.cfg['switch_input']
    except:
      return False

  def read_config(self):
    with open(self.config_path, 'r') as ymlfile:
      self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

  def write_config(self):
    with file(self.config_path, 'w') as ymlfile:
      yaml.dump(self.cfg, ymlfile)

    self.read_config()