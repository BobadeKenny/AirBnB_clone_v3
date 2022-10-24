#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_place(review_id):
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'text' not in request.json:
        abort(400, "Missing text")
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    obj = Review(**request.json)
    obj.place_id = place_id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    if not request.json:
        abort(400, "Not a JSON")
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    ignore = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for key, val in request.json.items():
        if key not in ignore:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict()), 200
