import logging
import signal
import time

from cellulariot import cellulariot


def handler(signum, frame):
    raise Exception("Timeout waiting for GPS location")


class SixFabSensors:
    def __init__(self, handler=None):
        self.node = cellulariot.CellularIoTApp()
        self.node.setupGPIO()
        self.gps_ready = False

    def __del__(self):
        self.node.turnOffGNSS()
        self.node.disable()
        del self.node

    def init_gps(self):
        if self.gps_ready == False:
            self.node.disable()
            time.sleep(2)
            self.node.enable()
            time.sleep(2)
            self.node.powerUp()
            time.sleep(5)
            self.node.turnOnGNSS()
            logging.getLogger().debug('waiting 30 seconds for GNSS to "warm up"')
            time.sleep(30)
            self.gps_ready = True

    def get_node(self):
        global node
        try:
            node
        except NameError:
            init()
        return node

    def get_temperature(self):
        return self.node.readTemp()

    def get_humidity(self):
        return self.node.readHum()

    def get_location(self):
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(50)
        try:
            self.init_gps()
            location = self.node.getFixedLocation()
            return location
        except Exception as e:
            logging.getLogger().debug("get_location error: {}".format(e))
            return False
