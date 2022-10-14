import logging
import RPi.GPIO as GPIO
from time import sleep

logger = logging.getLogger()

GM_OUTPUT_PIN = 17

class ServoOutput:
  def __init__(self, servo_on_time):
    self.setup_gpio()
    self.servo_on_time = servo_on_time

  def __del__(self):
    logger.warning('ServoOutput::__del__')
    self.pwm.stop()
    del self.pwm
    GPIO.cleanup()

  def set_servo_on_time(self, time):
    self.servo_on_time = time

  def setup_gpio(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GM_OUTPUT_PIN, GPIO.OUT)
    self.pwm = GPIO.PWM(GM_OUTPUT_PIN, 50)
    self.pwm.start(0)

  def servo_move(self, angle):
    duty = angle / 18 + 2
    logger.info("servo_move {} from {}".format(duty, angle))
    GPIO.output(GM_OUTPUT_PIN, True)
    self.pwm.ChangeDutyCycle(duty)
    sleep(self.servo_on_time)
    GPIO.output(GM_OUTPUT_PIN, False)
    self.pwm.ChangeDutyCycle(0)