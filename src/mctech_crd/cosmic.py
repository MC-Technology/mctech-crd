# Python libs
from collections import OrderedDict
import datetime
import getopt
import logging
import os
from pathlib import Path
import sys
from time import time, gmtime, sleep, strftime, localtime
from urllib.request import urlopen

# External libs
# from sixfab_sensors import SixFabSensors

# Our modules
from .config_reader import ConfigReader
from .gm_sensor import GMSensor
from .google_sheets import GoogleSheets
# import logging_config
from .media_player import MediaPlayer
from .midi_input import MidiInput
from .relay_output import RelayOutput
from .serial_number import get_serial_number
from .servo_output import ServoOutput
from .switch_input import SwitchInput
from .text_event_writer import TextEventWriter

logger = logging.getLogger()


def await_internet_access(max_retries=20, retry_delay=5):
  internet_accessible = False
  retry = 0

  while not internet_accessible and retry < max_retries:
    try:
      internet_accessible = bool(urlopen("http://google.com"))
    except:
      retry += 1
      logger.info(f"Network retry {retry}")
      sleep(retry_delay)
    else:
      logger.info(f"Internet accessible")

  return internet_accessible

def get_ip_address():
  try:
    fp = urlopen('https://api.ipify.org/')
    ip_address = fp.read()
    ip_address = ip_address.decode("utf8")
    fp.close()
  except:
    ip_address = 'no-network'

  return ip_address

def help():
  print ("{} --config=<config_file>".format(__file__))

def parse_args(argv):
  parsed_args = {}
  try:
    opts, args = getopt.getopt(argv,"h",["config="])
  except getopt.GetoptError:
    help()
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      help()
      sys.exit(0)
    elif opt in ("--config"):
      parsed_args['config_file'] = arg
  return parsed_args

def get_config(args):
  config_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../config/dev.yaml'))
  config_file = args.get('config_file', config_path)
  if os.path.isabs(config_file) == False:
    config_file = os.path.normpath(os.path.join(os.getcwd(), config_file))

  logger.info("Using config file {}".format(config_file))
  return ConfigReader(config_file)


def listen(argv):
  global logger

  last_time = 0
  servo_output = None

  parsed_args = parse_args(argv)

  config = get_config(parsed_args)

  min_interval = config.get_min_interval()
  servo_angle = 45

  location = config.get_location()

  network_config = config.network()
  google_config = config.google_logging()
  relay_config = config.get_relay_output()
  switch_config = config.get_switch_input()

  if config.has_media_player():
    logger.info('Using Media Player')
    player = MediaPlayer()

  if config.has_text_logging():
    logger.info('Using local text file logging')
    filepath = os.path.normpath(os.path.join(os.path.dirname(__file__), '../cosmic_pi_event.log'))
    text_log = TextEventWriter(filepath)

  google_sheets = None
  if google_config:
    await_internet_access(**network_config)
    try:
      google_sheets = GoogleSheets(google_config)
      logger.info('Using Google Sheets logging')
    except:
      logger.warning('Cannot use Google Sheets logging - check your network connection!')

  if relay_config:
    relay_output_pin = relay_config.get('gpio_pin', 24)
    logger.info("Using RelayOutput on {}".format(relay_output_pin))
    relay_output = RelayOutput(relay_output_pin)

  # gps_sensors = None
  # if config.has_gps_sensor():
  #   gps_sensors = SixFabSensors()
  #   logger.info("temperature is {}".format(gps_sensors.get_temperature()))
  #   gps_location = gps_sensors.get_location()
  #   if gps_location == False:
  #     logger.info('No GPS available!')
  #   else:
  #     location = gps_location

  serial_number = get_serial_number()
  ip_address = get_ip_address() or "no-network"
  logger.warning("IP is {}, serial_number: {}".format(ip_address, serial_number))

  logger.warning("location is {}".format(location))

  if config.has_media_player():
    player.play_media()

  def hit_counter(test=False):
    nonlocal last_time
    hit_time = time()
    iso_time = strftime("%Y-%m-%dT%H:%M:%S", localtime(hit_time))
    columns = [('ip_address', ip_address), ('location', location)]
    if test:
      columns.append(('test', 'TEST'))
    extra_fields = OrderedDict(columns)


    # These are all blocking - is that okay?
    if hit_time - last_time > min_interval:
      logger.info("Detected {}".format(hit_time))
      if google_sheets is not None:
        google_sheets.write_event(iso_time, serial_number, extra_fields)

      if config.has_text_logging():
        text_log.write_event(iso_time, serial_number, extra_fields)

      if config.has_media_player():
        player.play_media()

      if config.has_servo_motor():
        servo_output.servo_move(servo_angle)
        servo_output.servo_move(0)

      if relay_config:
        relay_output.relay_on(relay_config.get('on_time', 6))

      last_time = hit_time

  gm = GMSensor(handler=hit_counter)

  def test_hit(*args, **kwargs):
    logger.info("TEST HIT")
    hit_counter(test=True)

  if switch_config:
    # Pin diagram
    # https://www.jameco.com/Jameco/workshop/circuitnotes/raspberry-pi-circuit-note.html
    switch_input_pin = switch_config.get('gpio_pin', 23)
    switch_input = SwitchInput(switch_input_pin, handler=test_hit)

  midi_config = None
  if config.has_servo_motor():
    midi_config = config.get_midi_controls()
    servo_output = ServoOutput(midi_config.get('servo_on_time', 1))

    def midi_handler(message):
      nonlocal servo_angle, min_interval
      if message.type == 'control_change':
        if message.control == midi_config.get('sensitivity', 10):
          value = message.value
          sensitivity_seconds = midi_config.get('sensitivity_seconds', 1.0)
          min_interval = sensitivity_seconds * (value / 127.0)
          logger.info("min_interval set to {} from {}".format(min_interval, value))
        elif message.control == midi_config.get('servo_angle', 11):
          value = message.value
          angle_multiplier = midi_config.get('angle_multiplier', 90)
          servo_angle = angle_multiplier * (value / 127.0)
          logger.info("servo_angle set to {} from {}".format(servo_angle, value))
        elif message.control == midi_config.get('servo_on_ctrl', 91):
          value = message.value
          servo_on_time = 5.0 * (value / 127.0)
          logger.info("servo_on_time set to {} from {}".format(servo_on_time, value))
          servo_output.set_servo_on_time(servo_on_time)
      elif message.type == 'note_on':
        logger.info("note_on message {}".format(message))
        hit_counter()

    if midi_config:
      midi_in = MidiInput(midi_handler)

  last_time = time()

  if config.keyboard_trigger:
    try:
      import keyboard
    except ImportError:
      print("To run with keyboard_trigger you must run the script as root")
      sys.exit(1)
    print("TEST MODE: press enter on the rPi keyboard to trigger a hit")
    keyboard.on_press_key("enter", test_hit)

  try:
    logger.warning("Sensor initialized, waiting for input or CTRL+C to quit")
    while True:
      sleep(1)

  except KeyboardInterrupt:
    del gm
    if gps_sensors is not None:
      del gps_sensors
    if config.has_media_player():
      del player
    if google_sheets is not None:
      del google_sheets
    if midi_config is not None:
      del midi_in
    if switch_config:
      del switch_input
    if relay_config:
      del relay_output
    logger.warning("Bye!!")
    sys.exit(0)

if __name__ == "__main__":
  listen(sys.argv[1:])
