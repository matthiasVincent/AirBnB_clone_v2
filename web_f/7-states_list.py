#!/usr/bin/python3

"""
Script start a flask web application with
requirements:
    Listen on 0.0.0.0 port 5000,
    Use storage to fetch data from engines(FileStorage or DBStorage)
    Remove current session after each request using @app.teardown_appcontext
    on a given method
    Routes:
        /state_list: display a HTML page with state information
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


@app.route("/state_list", strict_slashes=False)
def state_list():
    """display state_list alphabetically in a HTML page"""
    all_state_dict = storage.all()
    all_state = [values for values in all_state_dict.values()]

    # print(all_state)
    return render_template("7-state_list.html", all_state=all_state)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
