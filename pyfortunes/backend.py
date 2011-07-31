""" This files contains the FortunesDB class,
which interacts with the fortunes database.

It is used by the FortunesServer to handle the
requests

"""

import os
import subprocess

class FortunesDB():
    """
    Initialiazed with a fortune directory.

    Can do stuff like:
     - print a fortune at random
     - add a new fortune
     - list fortune categories
    """
    def __init__(self, directory):
        self.directory = directory

    def get_categories(self):
        res = [x for x in os.listdir(self.directory) if not x.endswith(".dat")]
        res.sort()
        return res

    def add_fortune(self, category, text):
        if not category:
            raise Exception("category cannot be empty")
        if not text:
            raise Exception("text cannot be empty")
        if not text.endswith("\n"):
            text += "\n"
        filename = os.path.join(self.directory, category)
        with open(filename, "a", encoding='utf-8') as fp:
            fp.write("%\n")
            fp.write(text)

        output_ = subprocess.check_output(["strfile", filename])
        return True

    def get_fortune(self, category=None):
        """ Get a fortune.
        If category is not None, only use fortunes from the
        given category

        """
        cmd = ["fortune"]
        if category:
            if not category in self.get_categories():
                raise Exception("'%s' : no such category" % category)
            cmd.append(os.path.join(self.directory, category))
        else:
            cmd.append(self.directory)
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            return ""
        output = output.strip()
        return output.decode()

