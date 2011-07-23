""" An XML RPC server for a fortune database

"""

import os
import argparse
import xmlrpc.server

import pyfortunes

class FortunesServer(xmlrpc.server.SimpleXMLRPCServer):
    """
    Initialiazed with a fortune directory and a port

    Exposes methods from the backend's FortunesDB class

    """
    def __init__(self, directory, port=8080):
        self.directory = directory
        super().__init__(("0.0.0.0", port), logRequests=False)
        self.db = pyfortunes.backend.FortunesDB(directory)

    def add_fortune(self, category, text):
        return self.db.add_fortune(category, text)

    def get_categories(self):
        return self.db.get_categories()

    def get_fortune(self):
        return self.db.get_fortune()

    def get_fortune_from_category(self, category):
        return self.db.get_fortune(category=category)

    def get_fortunes_zip(self):
        """ Returns an url where to download the whole fortunes
        collection

        """
        return ""

    def _dispatch(self, method, params):
        """ Implements SimpleXMLRPCServer._dispatch.

        """
        # Every 'public' method is made available:
        if method.startswith("_"):
            return None
        func = getattr(self, method)
        return func(*params)


def run_server(directory, port):
    """ Runs a fortunes server

    """
    server = FortunesServer(directory, port)
    server.register_instance(server)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return

