""" An XML RPC client for a fortune database

"""
import os

import subprocess
import tempfile
import xmlrpc.client

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



def add_fortune(proxy):
    """ Add a new fortune

    """
    (fd, name) = tempfile.mkstemp()
    retcode = subprocess.call(["vim", name])
    if retcode != 0:
        return

    fp = os.fdopen(fd, "r")
    text = fp.read()
    fp.close()
    os.remove(name)

    if not text:
        print("Empty fortune, aborting")
        return

    categories = proxy.get_categories()
    print(":: Please select a category, or 'N' to add a new one")
    category = ask_category(categories)
    if not category:
        print("No category given, aborting")
        return

    proxy.add_fortune(category, text)


def get_proxy(url):
    """ Get an XML RPC server proxy from an URL """
    proxy = xmlrpc.client.ServerProxy(url)
    return proxy


if __name__ == "__main__":
    proxy = get_proxy("http://localhost:8080/")
    add_fortune(proxy)
