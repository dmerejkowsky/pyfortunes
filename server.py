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
application_root = os.environ.get("APPLICATION_ROOT")
if application_root:
    app.config["APPLICATION_ROOT"] = application_root
# Ugly hack:
else:
    app.config["APPLICATION_ROOT"] = ""


FORTUNES = None

def reload_fortunes():
    """ set the global FORTUNES variable
    called by the special route /reload

    """
    global FORTUNES
    pickle_path = os.environ["PICKLE_PATH"]
    with open(pickle_path, "rb") as fp:
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
    return "OK"

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
    return render_template("fortune.html", text=text,
                           index=(i + 1), category=category)

@app.route("/fortune/<category>")
def get_by_category(category=None):
    in_category = FORTUNES.get(category)
    if not in_category:
        abort(404)
    n = len(in_category)
    i = random.randint(0, n-1)
    text = in_category[i]
    return render_template("fortune.html", text=text,
                           index=(i + 1), category=category)

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
        return render_template("fortune.html", text=text,
                               index=(i + 1), category=category)
    else:
        abort(404)

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    # Call it at least once
    reload_fortunes()
    app.run(port=int(port))
