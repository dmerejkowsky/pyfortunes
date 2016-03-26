import os
import sys
import pickle
import random

from flask import Flask
from flask import Response
from flask import render_template
from flask import abort
from flask import request

import pyfortunes.config

app = Flask(__name__)


FORTUNES = None
PICKLE_PATH = None
PORT = 5000


def reload_fortunes():
    """ set the global FORTUNES variable
    called by the special route /reload

    """
    global FORTUNES
    with open(PICKLE_PATH, "rb") as fp:
        FORTUNES = pickle.load(fp)

def iter_all_fortunes():
    """ Generate a unique id, the category and the text for
    each fortune in the database

    """
    for category in sorted(FORTUNES.keys()):
        in_category = FORTUNES[category]
        for i, text in enumerate(in_category):
            yield (i, category, text)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reload")
def reload():
    reload_fortunes()
    return "OK\n"

@app.route("/search")
def search():
    pattern = request.args.get("pattern")
    if pattern:
        res = list()
        for i, category, text in iter_all_fortunes():
            if pattern in text:
                res.append((i, category, text))
        return render_template("search_results.html",
                pattern=pattern, fortunes=res)
    else:
        return render_template("search.html")


@app.route("/categories")
def show_categories():
    categories = list(FORTUNES.keys())
    categories.sort()
    return render_template("categories.html",
                           categories=categories)

@app.route("/fortune")
def get_random():
    n = sum(len(x) for x in FORTUNES.values())
    i = random.randint(0, n-1)

    (i, category, text) = list(iter_all_fortunes())[i]
    return render_fortune(text, i, category)

@app.route("/fortune/<category>")
def get_by_category(category=None):
    in_category = FORTUNES.get(category)
    if not in_category:
        abort(404)
    n = len(in_category)
    i = random.randint(0, n-1)
    text = in_category[i]
    return render_fortune(text, i, category)

@app.route("/fortune/<category>/<index>")
def get_by_category_and_index(category=None, index=None):
    try:
        i = int(index) - 1
    except ValueError:
        abort(404)
    in_category = FORTUNES.get(category)
    if not in_category:
        abort(404)
    n = len(in_category)
    if 0 <= i < n:
        text = in_category[i]
        return render_fortune(text, i, category)
    else:
        abort(404)

def render_fortune(text, index, category):
    """ Helper method to display a given fortune to the user
    the ?format argument can be given for each URL.

    Accepted values: `text` and `html` (the default)

    """
    format = request.args.get("format", "html")
    i = index + 1 # (more readable for humans :)
    if format == "html":
        return render_template("fortune.html", text=text,
                            index=i, category=category)
    else:
        res = text
        res += "\n[%s #%i]\n" % (category, i)
        return Response(res, mimetype="text/plain")

def setup():
    config = pyfortunes.config.get_config()
    if not config.has_section("server"):
        sys.exit("Could not find server config!")
    server_config = config["server"]

    global PICKLE_PATH
    PICKLE_PATH = server_config["pickle_path"]

    global PORT
    PORT = server_config.getint("port", 5000)

    app.debug = server_config.getboolean("debug", False)

    app.config["APPLICATION_ROOT"] = server_config.get("application_root", "")

    reload_fortunes()

def main():
    app.run(port=PORT)

# Make sure app is correctly setup when used with uwsgi
setup()

if __name__ == "__main__":
    main()
