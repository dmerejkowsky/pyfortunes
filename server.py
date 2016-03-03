import os
import sys
import pickle
import random

from flask import Flask
from flask import render_template
from flask import abort
from flask import request

app = Flask(__name__)
app.debug = os.environ.get("DEBUG")

def get_fortunes():
    pickle_path = os.environ["PICKLE_PATH"]
    with open(pickle_path, "rb") as fp:
        fortunes = pickle.load(fp)
    return fortunes


def iter_all_fortunes():
    """ Generate a unique id, the category and the text for
    each fortune in the database

    """
    fortunes = get_fortunes()
    for category in sorted(fortunes.keys()):
        in_category = fortunes[category]
        for i, text in enumerate(in_category):
            yield (i, category, text)

@app.route("/")
def index():
    return render_template("index.html")

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
    fortunes = get_fortunes()
    categories = list(fortunes.keys())
    categories.sort()
    return render_template("categories.html",
                           categories=categories)

@app.route("/fortune")
def get_random():
    fortunes = get_fortunes()
    n = sum(len(x) for x in fortunes.values())
    i = random.randint(0, n-1)

    (i, category, text) = list(iter_all_fortunes())[i]
    return render_template("fortune.html", text=text,
                           index=(i + 1), category=category)

@app.route("/fortune/<category>")
def get_by_category(category=None):
    fortunes = get_fortunes()
    in_category = fortunes.get(category)
    if not in_category:
        abort(404)
    n = len(in_category)
    i = random.randint(0, n-1)
    text = in_category[i]
    return render_template("fortune.html", text=text,
                           index=(i + 1), category=category)

@app.route("/fortune/<category>/<index>")
def get_by_category_and_index(category=None, index=None):
    fortunes = get_fortunes()
    try:
        i = int(index) - 1
    except ValueError:
        abort(404)
    in_category = fortunes.get(category)
    if not in_category:
        abort(404)
    n = len(in_category)
    if 0 <= i < n:
        text = in_category[i]
        return render_template("fortune.html", text=text,
                               index=(i + 1), category=category)
    else:
        abort(404)

port = os.environ.get("PORT", 5000)
app.run(port=int(port))
