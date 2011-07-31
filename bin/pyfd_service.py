""" A windows service to run the server

"""

import os
import sys
import argparse
import configparser

WITH_PYF=True

try:
    import pyfortunes
    from pyfortunes.thirdparty import winservice
except ImportError as e:
    WITH_PYF=False
    pass


def get_config_file():
    """ Try to get a config file using
    the path of the current file

    """
    server_file = pyfortunes.server.__file__
    server_dir = os.path.dirname(server_file)
    pyfd_conf = os.path.join(server_dir, "pyfd.conf")
    return pyfd_conf

def die(msg):
    """ Exit the service with an error message

    """
    winservice.error(msg)
    sys.exit(1)


class PyFortunesService(winservice.Service):
    """ The pyfortunes Service

    """
    def __init__(self, *args):
        super().__init__(*args)
        config_file = get_config_file()
        config = configparser.ConfigParser()
        config.read(config_file)
        if not 'pyfd' in config:
            die("No [pyfd] section in config file")
        pyfd_conf = config['pyfd']
        port = pyfd_conf.get('port', '8080')
        directory = pyfd_conf.get('directory')
        if not directory:
            die("No directory setting in config file")
        port      = 8080
        self.server = pyfortunes.server.FortunesServer(directory, port)

    def start(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


def main():
    """ Install and start the PyFortunes daemon

    """
    winservice.instart(PyFortunesService, "PyFortunes", "PyFortunes Service")

if __name__ == "__main__":
    main()


