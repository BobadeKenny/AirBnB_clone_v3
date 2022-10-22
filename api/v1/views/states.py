#!/usr/bin/python3
"""
starts a Flask web application
"""
from urllib import response
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    states_dict = []
    for val in storage.all(State).values():
        states_dict.append(val.to_dict())
    return jsonify(states_dict)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    obj = State(**request.json)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    if not request.json:
        abort(400, "Not a JSON")
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    ignore = ["id", "created_at", "updated_at"]
    for key, val in request.json.items():
        if key not in ignore:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict()), 200
