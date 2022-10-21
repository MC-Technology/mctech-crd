import mido
import logging

logger = logging.getLogger()

class MidiInput:
  def __init__(self, handler=None):
    self.control_handler = handler
    self.setup_inputs(handler)

  def __del__(self):
    logger.warning('MidiControls::__del__')
    self.inport.callback = None
    self.inport.close()

  def setup_inputs(self, handler):
    ports = mido.get_input_names()

    def callback(message):
      if self.input_handler:
        self.input_handler(message)

    self.inport = mido.open_input(ports[0], callback=callback)

  def input_handler(self, message):
    self.control_handler(message)