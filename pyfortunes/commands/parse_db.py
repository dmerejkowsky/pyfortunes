""" Regenerate the serialized fortunes when the db changes """
import sys
import pickle

import pyfortunes.config
import pyfortunes.db


def main():
    db = pyfortunes.db.FortuneDB()
    if "--no-sync" not in sys.argv:
        db.sync()
    db.parse_fortunes()
    config = pyfortunes.config.get_config()
    output = config["server"]["pickle_path"]
    with open(output, "wb") as fp:
        print("Dumping ...", end="")
        pickle.dump(db.fortunes, fp)
        print(" OK")
