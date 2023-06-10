#!/usr/bin/python3
"""Check the status of api"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.review import Review


objects = {
    Amenity: "amenities",
    City: "cities",
    Place: "places",
    User: "users",
    State: "states",
    Review: "reviews"
    }

@app_views.route('/status')
def status():
    """status function"""
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def stats():
    """return the stats of objects"""
    my_stats = { }

    for k, v in objects.items():
        my_stats[v] = storage.count(k)

    return jsonify(my_stats)
