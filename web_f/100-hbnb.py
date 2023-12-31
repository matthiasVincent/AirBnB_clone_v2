#!/usr/bin/python3

"""
Script start a flask web application with
requirements:
    Listen on 0.0.0.0 port 5000,
    Use storage to fetch data from engines(FileStorage or DBStorage)
    Remove current session after each request using @app.teardown_appcontext
    on a given method
    Routes:
        /hbnb: display a HTML page with dynamic data
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


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """display state_list alphabetically in a HTML page"""
    all_state_dict = storage.all("State")
    all_amenity_dict = storage.all("Amenity")
    all_places_dict = storage.all("Place")
    all_state = [values for values in all_state_dict.values()]
    all_amenity = [values for values in all_amenity_dict.values()]
    all_place = [values for values in all_places_dict.values()]

    # print(all_state)
    return render_template(
        "100-hbnb.html",
        all_state=all_state, all_amenity=all_amenity, all_place=all_place
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
