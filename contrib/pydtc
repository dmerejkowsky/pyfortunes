#!/usr/bin/python3
import re
import sys
import argparse
import subprocess

from bs4 import BeautifulSoup
import requests
import textwrap

import pyfortunes

def get_quote(id):
    url = "http://danstonchat.com/%s.html" % id
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html)
    # The quote is in the first <a> link that points to
    # self url ...
    self_links = soup("a", href="/%s.html" % id)
    if not self_links:
        print("no quote found?")
        return
    res = ""
    quote = self_links[0]
    # Quote is: <span class > for the pseudo, then some text, then <br />
    # Get only the pseudo, but keep the br and wrap the quote at
    # 80
    reply = ""
    for child in quote.children:
        if hasattr(child, "name"):
            if child.name == "span":
                reply += child.text
            if child.name == "br":
                reply = ""
                res += "\n"
        else:
            res += "\n".join(textwrap.wrap(reply + child))
    res += "\n"
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    url = args.url
    ns = argparse.Namespace(url=None)
    srv_url = pyfortunes.client.get_url(ns)
    quote = get_quote(url)
    proxy = pyfortunes.client.get_proxy(srv_url)
    pyfortunes.client.add_fortune(proxy, category="bash", text=quote)

if __name__ == "__main__":
    main()
