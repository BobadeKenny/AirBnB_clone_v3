#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    users = []
    for val in storage.all(User).values():
        users.append(val.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/users/<user_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    if not request.json:
        abort(400, "Not a JSON")
    if 'email' not in request.json:
        abort(400, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")
    obj = User(**request.json)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    if not request.json:
        abort(400, "Not a JSON")
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    ignore = ["id", "email", "created_at", "updated_at"]
    for key, val in request.json.items():
        if key not in ignore:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict()), 200
