#!/usr/bin/python3
"""Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
Routes:
    /states: HTML page with a list of all State objects.
    /states/<id>: HTML page displaying the given state with <id>.
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states_list():
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template("9-states.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def state_cities(id):
    state = storage.get(State, id)
    if state:
        return render_template("9-states_cities.html", state=state)
    else:
        return render_template("9-not_found.html")


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
