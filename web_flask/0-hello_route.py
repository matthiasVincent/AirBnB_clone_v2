#!/usr/bin/python3

"""
Script start a flask web application with
requirements:
    listen on 0.0.0.0 port 5000,
    Routes:
        /: display "Hello HBNB!"
    required to use the option, strict_slashes=False
"""

from flask import Flask

app = Flask(__file__)


@app.route("/", strict_slashes=False)
def hello():
    """display Hello HBNB!"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
