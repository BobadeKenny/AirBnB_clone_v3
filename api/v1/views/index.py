#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import jsonify, make_response
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status", strict_slashes=False)
def get_status():
    return jsonify({'status': 'OK'})


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })


@app_views.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Not Found"}), 404)
