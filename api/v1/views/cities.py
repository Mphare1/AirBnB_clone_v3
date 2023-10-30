#!/usr/bin/python3
"""A view for cities"""
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request

@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=["GET"])
def get_cities(state_id):
    """Retreieve the cities connected to a state object"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
        return jsonify({"error": "Not found"})

    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """Get a city by id"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)
        return jsonify({"error": "Not found"})

    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """Delete a city object"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)
        return jsonify({"error": "Not found"})
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=["POST"])
def create_city(state_id):
    """Create a new city in state object"""

    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    if 'name' not in request.json:
        abort(400)
        return jsonify({"error": "Missing name"})

    state = storage.get(State, state_id)
    if not state:
        abort(404)
        return jsonify({"error": "Not found"})
    new_city = City(**request.get_json())
    setattr(new_city, "state_id", state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """Update a city"""

    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    city_json = request.get_json(silent=True)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
        return jsonify({"error": "Not found"})

    for k, v in city_json.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
