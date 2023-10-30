#!/usr/bin/python3
"""A Flask API app"""

from os import getenv
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(code):
    """Close the current session"""
    storage.close()

@app.errorhandler(404)
def not_found(e):
    """Not found page"""
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'), \
            port=int(getenv('HBNB_API_PORT', '5000')), threaded=True)
