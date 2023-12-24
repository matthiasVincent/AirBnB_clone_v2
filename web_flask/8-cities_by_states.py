#!/usr/bin/python3

"""
Script start a flask web application with
requirements:
    Listen on 0.0.0.0 port 5000,
    Use storage to fetch data from engines(FileStorage or DBStorage)
    Remove current session after each request using @app.teardown_appcontext
    on a given method
    Routes:
        /cities_by_states: display a HTML page with state and city information
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


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """display state_list alphabetically in a HTML page"""
    all_state_dict = storage.all("State")
    all_state = [values for values in all_state_dict.values()]

    # print(all_state)
    return render_template("8-cities_by_states.html", all_state=all_state)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
