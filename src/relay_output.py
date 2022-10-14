import logging
import RPi.GPIO as GPIO
from time import sleep
import threading

logger = logging.getLogger()

class RelayOutput:
  def __init__(self, relay_output_pin):
    self.setup_gpio(relay_output_pin)
    self.waitingForRelayToFinish = False

  def __del__(self):
    logger.warning('RelayOutput::__del__')
    GPIO.output(self.relay_output_pin, False)
    GPIO.cleanup()

  def setup_gpio(self, relay_output_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_output_pin, GPIO.OUT)
    self.relay_output_pin = relay_output_pin

  def relay_on(self, on_time):
    if self.waitingForRelayToFinish == True:
      return

    logger.info("relay_on for {}".format(on_time))
    GPIO.output(self.relay_output_pin, True)
    # sleep(on_time)
    # GPIO.output(self.relay_output_pin, False)
    # logger.info("relay off")

    def timeoutHandler():
        GPIO.output(self.relay_output_pin, False)
        logger.info("relay off")
        self.waitingForRelayToFinish = False

    timer = threading.Timer(on_time, timeoutHandler)
    timer.start()
    self.waitingForRelayToFinish = True