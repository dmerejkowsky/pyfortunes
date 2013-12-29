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
    response.encoding = 'utf-8'
    html = response.text
    return extract_quote(html, id)

def extract_quote(html, id):
    soup = BeautifulSoup(html)
    url = "http://danstonchat.com/%s.html" % id
    # The quote is in the first <a> link that points to
    # self url ...
    self_links = soup("a", href=url)
    if not self_links:
        return
    res = ""
    quote = self_links[0]
    # Quote is: <span class > for the pseudo, then some text, then <br />
    # Get only the pseudo, but keep the br and wrap the quote at
    # 80
    res = ""
    reply = ""
    for child in quote.children:
        if not child.name:
            reply += child
        if child.name == "span":
            reply = child.text
        if child.name == "br":
            res += "\n".join(textwrap.wrap(reply))
            res += "\n"
            reply = ""
    # there's no final <br />
    if reply:
        res += "\n".join(textwrap.wrap(reply))
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
    if not quote:
        sys.exit("no quote found")
    proxy = pyfortunes.client.get_proxy(srv_url)
    pyfortunes.client.add_fortune(proxy, category="bash", text=quote)

if __name__ == "__main__":
    main()
