"""
Uses RPi.GPIO Python module to receive sensor input
https://pypi.org/project/RPi.GPIO
"""

import logging
import RPi.GPIO as GPIO
from time import sleep

logger = logging.getLogger()

GM_INPUT_PIN = 5
LED_OUTPUT_PIN = 22

class GMSensor:
  def __init__(self, handler=None):
    self.event_handler = handler
    self.setup_gpio()

  def __del__(self):
    logger.warning('GMSensor::__del__')
    GPIO.cleanup()

  def input_handler(self, channel):
    if channel == GM_INPUT_PIN:
      self.event_handler()
      self.flash_led()

  def setup_gpio(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GM_INPUT_PIN, GPIO.IN)
    GPIO.setup(LED_OUTPUT_PIN,GPIO.OUT)

    def callback(channel):
      if self.input_handler:
        self.input_handler(channel)

    GPIO.add_event_detect(GM_INPUT_PIN, GPIO.RISING, callback=callback)

  def flash_led(self):
    GPIO.output(LED_OUTPUT_PIN,GPIO.HIGH)
    sleep(3)
    GPIO.output(LED_OUTPUT_PIN,GPIO.LOW)
