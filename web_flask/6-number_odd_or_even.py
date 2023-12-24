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
        /number/<n>: display "n is a number" only if n is an integer
        /number_template/<n>: display a HTML_page only if n is an integer
        /number_odd_or_even/<n>: display a HTML_page
        only if n is an integer(even or odd)
    required to use the option, strict_slashes=False
"""

from flask import Flask
from flask import render_template

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


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """display, n is a number only if n is an integer"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def template_route(n):
    """render a template with n is an integer in a H1 tag"""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even_route(n):
    """render a template with n is an integer in a H1 tag"""
    if n % 2 == 0:
        response = "{} is even".format(n)
    else:
        response = "{} is odd".format(n)
    return render_template("6-number_odd_or_even.html", response=response)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
