#!/usr/bin/python3
"""A view for places"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=["GET"])
def get_places(city_id):
    """Retrieve the places within a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
        return jsonify({"error": "Not found"})
    places = storage.all(Place)
    place_list = []

    for k, v in places.items():
        if v.city_id == city_id:
            place_list.append(v.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=["GET"])
def get_place(place_id):
    """Retrieve a place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
        return jsonify({"error": "Not found"})

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """Delete place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
        return jsonify({"error": "Not found"})
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """Create place based on city id"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    if 'user_id' not in request.json:
        abort(400)
        return jsonify({"error": "Missing user_id"})
    if 'name' not in request.json:
        abort(400)
        return jsonify({"error": "Mising name"})

    city = storage.get(City, city_id)
    if not city:
        abort(404)
        return jsonify({"error": "Not found"})
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
        return jsonify({"error": "Not found"})

    new_place = Place(**request.get_json())
    setattr(new_place, "city_id", city_id)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """Update place info"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    place_atr = request.get_json(silent=True)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
        return jsonify({"error": "Not found"})

    for k, v in place_atr.items():
        if k not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, k, v)

    place.save()
    return jsonify(place.to_dict()), 200
