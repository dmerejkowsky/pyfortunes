""" Import quote from danstonchat.com """
import argparse

from bs4 import BeautifulSoup
import requests
import textwrap

from pyfortunes.db import FortuneDB


def get_quote(id):
    url = "http://danstonchat.com/%s.html" % id
    response = requests.get(url)
    response.encoding = "utf-8"
    html = response.text
    return extract_quote(html)


def extract_quote(html):
    soup = BeautifulSoup(html, "html.parser")
    desc = soup.find("meta", {"name": "description"})
    return desc.attrs["content"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("id")
    args = parser.parse_args()
    quote_id = args.id
    fortunes_db = FortuneDB()
    quote = get_quote(quote_id)
    fortunes_db.append_and_push(quote, category="bash")
