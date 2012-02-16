""" An XML RPC client for a fortune database

"""
import os
import sys

import configparser
import subprocess
import tempfile
import xmlrpc.client

DEFAULT_URL = "http://localhost:8080"

def ask_category(choices):
    """Ask the user to choose from a list of choices,
    add allow to add another choice to the list

    """
    for i, choice in enumerate(choices):
        print("%3d. %s" % ((i+1), choice))
    keep_asking = True
    res = None
    while keep_asking:
        answer = input("> ")
        if not answer:
            return choices[0]
        if answer == "N":
            print("Please enter a new category")
            res = input("> ")
            return res
        try:
            index = int(answer)
        except ValueError:
            print("Please enter number")
            continue
        if index not in range(1, len(choices)+1):
            print("%i is out of range" % index)
            continue
        res = choices[index-1]
        keep_asking = False

    return res



def add_fortune(proxy, text=None, category=None):
    """ Add a new fortune.

    If fortune is not given, fire up and editor to
    let the user enter one.

    If category is not given, ask the list of the categories
    to the server and let the user choose one.

    """
    on_win = sys.platform.startswith("win")
    if not text:
        if on_win:
            tmp = os.environ["TEMP"]
        else:
            tmp = "/tmp"
        tmp_file = os.path.join(tmp, "fortune.txt")
        # FIXME: do not hard code text editor
        if on_win:
            retcode = subprocess.call([r"C:\Program Files (x86)\Vim\vim73\gvim.exe", tmp_file])
        else:
            retcode = subprocess.call(["vim", tmp_file])
        if retcode != 0:
            return
        if not os.path.exists(tmp_file):
            print("No fortune given, aborting")
            return
        with open(tmp_file, "r", encoding='utf-8') as fp:
            text = fp.read()
        os.remove(tmp_file)

    if not text:
        print("Empty fortune, aborting")
        return

    if not category:
        categories = proxy.get_categories()
        print(":: Please select a category, or 'N' to add a new one")
        category = ask_category(categories)
        if not category:
            print("No category given, aborting")
            return

    print("Adding new fortune:\n{}[{}]".format(text, category))
    proxy.add_fortune(category, text)

def configure_parser(parser):
    """ Build a suitable argparse.ArgumentParser for
    a client

    """
    parser.add_argument("--url", help="Pyfortunes server url. "
        "Defaults to %s" % DEFAULT_URL)

def get_url(args):
    """ Get the url to use, using a argparse.Namespace
    object

    """
    if args.url is not None:
        return args.url
    conf_path = os.path.expanduser("~/.config/pyfortunes.cfg")
    parser = configparser.ConfigParser()
    parser.read(conf_path)
    if not parser.has_option("server", "url"):
        return DEFAULT_URL
    url = parser.get("server", "url")
    return url



def get_proxy(url=DEFAULT_URL):
    """ Get an XML RPC server proxy from an URL """
    proxy = xmlrpc.client.ServerProxy(url)
    return proxy


def get_fortune(proxy, category=None):
    if category is None:
        return proxy.get_fortune()
    else:
        return proxy.get_fortune_from_category(category)

if __name__ == "__main__":
    proxy = get_proxy()
    add_fortune(proxy)
