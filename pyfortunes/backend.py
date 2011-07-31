""" This files contains the FortunesDB class,
which interacts with the fortunes database.

It is used by the FortunesServer to handle the
requests

"""

import os
import random

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

        return True
    def get_fortune(self, category=None):
        """ Get a fortune.
        If category is not None, only use fortunes from the
        given category

        """
        categories = self.get_categories()
        if not categories:
            return ""
        if category:
            if not category in categories:
                raise Exception("'%s' : no such category" % category)
        else:
            category = random.choice(categories)

        filename = os.path.join(self.directory, category)
        fortunes = list()
        cur_fortune = ""
        with open(filename, "r", encoding='utf-8') as fp:
            for line in fp:
                if line == "%\n":
                    if cur_fortune:
                        fortunes.append(cur_fortune)
                    cur_fortune = ""
                else:
                    cur_fortune += line
        # If file does not end with '%\n', we can have one
        # fortune left:
        if cur_fortune:
            fortunes.append(cur_fortune)
        fortune = random.choice(fortunes)
        # Huge improvement from the 'fortune' executable:
        # also display the category from which the fortune came from
        return fortune + "[%s]" % category
