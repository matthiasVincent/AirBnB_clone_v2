#!/usr/bin/python3

"""
Script start a flask web application with
requirements:
    Listen on 0.0.0.0 port 5000,
    Use storage to fetch data from engines(FileStorage or DBStorage)
    Remove current session after each request using @app.teardown_appcontext
    on a given method
    Routes:
        /states: display a HTML page with state information
        /states/<id>: display a HTML page with a single state
        information and its linked cities
    required to use the option, strict_slashes=False
"""

from flask import Flask
from models import storage
from flask import render_template

app = Flask(__file__, template_folder="web_flask/templates")


@app.teardown_appcontext
def teardown(exc):
    """remove the current sqlalchemy session"""
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    """display state_list alphabetically in a HTML page"""
    all_state_dict = storage.all("State")
    all_state = [values for values in all_state_dict.values()]
    return render_template("9-states.html", all_state=all_state)


@app.route("/states/<id>", strict_slashes=False)
def single_state(id):
    """display state_list alphabetically in a HTML page"""
    all_state_dict = storage.all("State")
    state = all_state_dict.get('State.{}'.format(id), None)
    return render_template("9-states.html", state=state)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
