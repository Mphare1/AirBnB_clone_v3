#!/usr/bin/python3
"""amenities"""
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route('/amenities', strict_slashes=False, methods=["GET"])
def all_amenities():
    """Retrieve the list of all amenities"""
    amenities = storage.all(Amenity)
    amenity_list = []

    for k, v in amenities.items():
        amenity_list.append(v.to_dict())

    return jsonify(amenity_list)

@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["GET"])
def get_amenity(amenity_id):
    """Retrieve amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
        return jsonify({"error": "Not found"})
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
        return jsonify({"error": "Not found"})
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', strict_slashes=False, methods=["POST"])
def create_amenity():
    """Create a new amenity"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    if 'name' not in request.json:
        abort(400)
        return jsonify({"error": "Missing name"})

    amenity = Amenity(**request.get_json())
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    """Update amenity info"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    amenity_atr = request.get_json(silent=True)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
        return jsonify({"error": "Not found"})

    for k, v in amenity_atr.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
