import sys
import configparser
from xdg import BaseDirectory

def get_config():
    config_path = BaseDirectory.load_first_config("pyfortunes.cfg")
    if not config_path:
        sys.exit("pyfortunes.cfg not found")
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
