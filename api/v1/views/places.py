#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def get_places(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/places/<place_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    obj = Place(**request.json)
    obj.city_id = city_id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    if not request.json:
        abort(400, "Not a JSON")
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    ignore = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for key, val in request.json.items():
        if key not in ignore:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict()), 200
