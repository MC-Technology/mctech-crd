import logging
from time import sleep

try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO


logger = logging.getLogger()

LED_OUTPUT_PIN = 22


class SwitchInput:
    def __init__(self, switch_input_pin, handler=None):
        self.event_handler = handler
        self.setup_gpio(switch_input_pin)

    def __del__(self):
        logger.warning("SwitchInput::__del__")
        GPIO.cleanup()

    def input_handler(self, channel):
        if channel == self.switch_input_pin:
            logger.info("SwitchInput::input_handler")
            self.event_handler()

    def setup_gpio(self, switch_input_pin):
        self.switch_input_pin = switch_input_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch_input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        def callback(channel):
            if self.input_handler:
                self.input_handler(channel)

        GPIO.add_event_detect(
            self.switch_input_pin, GPIO.FALLING, callback=callback, bouncetime=2500
        )
