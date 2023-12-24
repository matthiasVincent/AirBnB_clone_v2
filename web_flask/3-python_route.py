#!/usr/bin/python3

"""
Script start a flask web application with
requirements:
    listen on 0.0.0.0 port 5000,
    Routes:
        /: display "Hello HBNB!"
        /hbnb: display "HBNB"
        /c/<text>: display "C" followed by the
        the value of the text variable(underscore replace with space)
        /python/<text>: display "Python", followed bt the value of text
        variable(relace underscore with space)
         default value of text is "is cool"
    required to use the option, strict_slashes=False
"""

from flask import Flask

app = Flask(__file__)


@app.route("/", strict_slashes=False)
def hello():
    """display Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """display HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """display "C" followed by the value of the text variable"""
    new_text = text.replace("_", " ")
    response = "C {}".format(new_text)
    return response


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is_cool"):
    """display "Python" followed by the value of the text variable"""
    new_text = text.replace("_", " ")
    response = "Python {}".format(new_text)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
