""" This files contains the FortunesDB class,
which interacts with the fortunes database.

It is used by the FortunesServer to handle the
requests

"""

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
        return ["misc", "jokes", "movies"]

    def add_fortune(self, category, text):
        print "Adding", category, text
        return True

