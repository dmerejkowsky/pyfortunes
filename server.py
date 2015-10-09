import os
import sys
import pickle
import random

from flask import Flask
from flask import render_template
from flask import abort

app = Flask(__name__)
app.debug = os.environ.get("DEBUG")

pickle_path = os.environ["PICKLE_PATH"]
with open(pickle_path, "rb") as fp:
    fortunes = pickle.load(fp)

categories = list(fortunes.keys())
categories.sort()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/categories")
def show_categories():
    return render_template("categories.html",
                           categories=categories)

@app.route("/fortune")
def get_random():
    n = sum(len(x) for x in fortunes.values())
    i = random.randint(0, n-1)
    def iter_all():
        for category in fortunes.keys():
            in_category = fortunes[category]
            for i, text in enumerate(in_category):
                yield (i, category, text)

    (i, category, text) = list(iter_all())[i]
    return render_template("fortune.html", text=text,
                           index=(i + 1), category=category)

@app.route("/fortune/<category>")
def get_by_category(category=None):
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
