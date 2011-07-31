""" A windows service to run the server

"""

import os
import sys
import argparse
import configparser

sys.path.insert(0, r"c:\Users\yannick\work\pyfortunes")

WITH_PYF=True

try:
    import pyfortunes
    from pyfortunes.thirdparty import winservice
except ImportError as e:
    WITH_PYF=False
    pass


class PyFortunesService(winservice.Service):
    """ The pyfortunes Service

    """
    def __init__(self, *args):
        super().__init__(*args)
        # FIXME: read those from a config file
        # TODO: find a way to find the config file ...
        directory = r"c:\Users\yannick\fortunes"
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


