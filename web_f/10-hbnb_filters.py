#!/usr/bin/python3

"""
Script start a flask web application with
requirements:
    Listen on 0.0.0.0 port 5000,
    Use storage to fetch data from engines(FileStorage or DBStorage)
    Remove current session after each request using @app.teardown_appcontext
    on a given method
    Routes:
        /hbnb_filters: display a HTML page with state
        and amenity information
    required to use the option, strict_slashes=False
"""

from flask import Flask
from models import storage
from flask import render_template
app = Flask(
    __file__,
    template_folder="web_flask/templates",
    static_folder="web_flask/static"
    )


@app.teardown_appcontext
def teardown(exc):
    """remove the current sqlalchemy session"""
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """display state_list alphabetically in a HTML page"""
    all_state_dict = storage.all("State")
    all_amenity_dict = storage.all("Amenity")
    all_state = [values for values in all_state_dict.values()]
    all_amenity = [values for values in all_amenity_dict.values()]
    return render_template(
        "10-hbnb_filters.html",
        all_state=all_state, all_amenity=all_amenity
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
