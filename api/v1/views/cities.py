#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def get_cites(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
def create_city(state_id):
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    obj = City(**request.json)
    obj.state_id = state_id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    if not request.json:
        abort(400, "Not a JSON")
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    ignore = ["id", "created_at", "updated_at"]
    for key, val in request.json.items():
        if key not in ignore:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict()), 200
