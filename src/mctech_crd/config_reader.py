import yaml
import logging
import os

logger = logging.getLogger()


class ConfigReader:
    """
    Reads configuration for the CRD listener from a yaml file
    """
    def __init__(self, config_path):
        self.cfg = []
        self.config_path = self.get_config_file_path(config_path)
        self.read_config()

    @staticmethod
    def get_config_file_path(config_path):
        """
        Config file will come from the following in descending precedence

        - cosmic listen --config
        - ./config_default/<cosmic listen --config>.yaml
        - COSMIC_CONFIG env var
        - ./config_default/mct_array
        """
        config_file = ""
        try:
            if config_path:
                if ".yaml" in config_path or ".yml" in config_path:
                    config_file = os.path.normpath(config_path)
                    # ensure path is absolute
                    if os.path.isabs(config_file) == False:
                        config_file = os.path.normpath(os.path.join(os.getcwd(), config_file))
                    logger.info(f"Using config file {config_file}")
                else:
                    # relative path should instead select a default config file, eg 'dev.yaml'
                    config_file = os.path.join(os.path.dirname(__file__), f"config_default/{config_path}.yaml")
                    logger.info(f"Using default config {config_path}.yaml")
        except:
            pass

        # provide a default
        if not os.path.exists(config_file):
            config_file = os.path.join(os.path.dirname(__file__), "config_default/mct_array.yaml")
            logger.info("Defaulting to dev config")

        return config_file

    def read_config(self):
        with open(self.config_path, "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    def write_config(self):
        with file(self.config_path, "w") as ymlfile:
            yaml.dump(self.cfg, ymlfile)

        self.read_config()

    def keyboard_trigger(self):
        return self.cfg.get("keyboard_trigger", 0)

    def get_logging(self):
        return self.cfg["logging"]

    def get_location(self):
        return self.cfg["location"]

    def get_min_interval(self):
        try:
            return self.cfg["min_interval"]
        except:
            return 0

    def set_location(self, location):
        self.cfg["location"] = location

    def has_media_player(self):
        try:
            return self.cfg["media_player"]
        except:
            return False

    def network(self):
        try:
            return self.cfg["network"]
        except:
            return {}

    def google_logging(self):
        return self.cfg.get("google_logging", None)

    def has_text_logging(self):
        try:
            return self.cfg["text_logging"]
        except:
            return False

    def has_gps_sensor(self):
        try:
            return self.cfg["gps_sensor"]
        except:
            return False

    def get_midi_controls(self):
        return self.cfg["midi_controls"]

    def has_servo_motor(self):
        try:
            return self.cfg["servo_motor"]
        except:
            return False

    def get_relay_output(self):
        try:
            return self.cfg["relay_output"]
        except:
            return False

    def get_switch_input(self):
        try:
            return self.cfg["switch_input"]
        except:
            return False
