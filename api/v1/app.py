#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask
from flask import jsonify, make_response
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
