""" Testing backend

"""


import os
import shutil
import socket
import tempfile
import threading
import unittest
import xmlrpc.client

import pyfortunes

# Small helper functions:
def _assert_exists(testcase, filename):
    """ Assert that a filename exists

    """
    testcase.assertTrue(os.path.exists(filename),
        "%s does not exists" % filename)

class BackendTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def get_db(self):
        return pyfortunes.backend.FortunesDB(self.tmp_dir)

    def test_create_fortune(self):
        db = self.get_db()
        db.add_fortune("quotes", "This is a quote")
        quotes = os.path.join(self.tmp_dir, "quotes")
        with open(quotes, "r") as fp:
            contents = fp.read()
        self.assertEqual(contents, "%\nThis is a quote\n")

    def test_add_to_existing_category(self):
        quotes = os.path.join(self.tmp_dir, "quotes")
        with open(quotes, "w") as fp:
            fp.write("This is the first quote\n")
        db = self.get_db()
        db.add_fortune("quotes", "This is a second quote")
        with open(quotes, "r") as fp:
            contents = fp.read()
        self.assertEqual(contents, """This is the first quote
%
This is a second quote
""")


    def test_get_categories(self):
        categories = ["jokes", "quotes"]
        for category in categories:
            filename = os.path.join(self.tmp_dir, category)
            with open(filename, "w") as fp:
                fp.write("\n")
            with open(filename + ".dat", "w") as fp:
                fp.write("\n")

        db = self.get_db()
        self.assertEqual(db.get_categories(), categories)

    def test_get_categories_after_adding_a_new_one(self):
        categories = ["jokes", "quotes"]
        for category in categories:
            filename = os.path.join(self.tmp_dir, category)
            with open(filename, "w") as fp:
                fp.write("\n")
            with open(filename + ".dat", "w") as fp:
                fp.write("\n")

        db = self.get_db()
        self.assertEqual(db.get_categories(), categories)

        db.add_fortune("movies", """Steve McCroskey: Looks like I picked the wrong week to quit amphetamines.
        -- Airplane !
""")

        self.assertEqual(db.get_categories(), ["jokes", "movies", "quotes"])


    def test_get_fortune(self):
        db = self.get_db()
        self.assertEqual(db.get_fortune(), "")
        db.add_fortune("jokes", "This is a joke")
        self.assertEqual(db.get_fortune(), "This is a joke\n[jokes]")
        db.add_fortune("quotes", "This is a quote")
        self.assertEqual(db.get_fortune(category="quotes"),
            "This is a quote\n[quotes]")




class ServerThread(threading.Thread):
    def __init__(self, server):
        super().__init__(name="ServerThread")
        self.server = server
    def run(self):
        self.server.serve_forever()

class ServerTest(unittest.TestCase):
    def  setUp(self):
        # Find a free port:
        sock = socket.socket()
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        self.port = port
        tmp_dir = tempfile.mkdtemp()
        self.server = pyfortunes.server.FortunesServer(tmp_dir, port=self.port)
        self.server_thread = ServerThread(self.server)
        self.server_thread.start()

    def test_server_api(self):
        url = "http://localhost:%d" % self.port
        proxy = pyfortunes.client.get_proxy(url)

        self.assertRaises(xmlrpc.client.Fault, proxy.does_not_exists)
        self.assertRaises(xmlrpc.client.Fault, proxy.add_fortune,
            "", "This is a fortune without category")
        self.assertRaises(xmlrpc.client.Fault, proxy.add_fortune,
            "jokes", "")

        self.assertEqual(proxy.get_categories(), list())

        proxy.add_fortune("jokes", "This is a joke")
        self.assertEqual(proxy.get_categories(), ["jokes"])

        fortune = proxy.get_fortune()
        self.assertEqual(fortune, "This is a joke\n[jokes]")

        proxy.add_fortune("quotes", "This is a quote")
        self.assertEqual(proxy.get_categories(), ["jokes", "quotes"])
        fortune = proxy.get_fortune_from_category("jokes")
        self.assertEqual(fortune, "This is a joke\n[jokes]")

        self.assertRaises(xmlrpc.client.Fault,
            proxy.get_fortune_from_category, "doesnotexist")



    def tearDown(self):
        self.server.shutdown()
        self.server_thread.join()


if __name__ == "__main__":
    unittest.main()
