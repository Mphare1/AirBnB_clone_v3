#!/usr/bin/python3
"""users"""

from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views

@app_views.route('/users', strict_slashes=False, methods=["GET"])
def all_users():
    """Retrieve a list of all user objects"""
    users = storage.all(User)
    users_list = []

    for k, v in users.items():
        users_list.append(v.to_dict())

    return jsonify(users_list)

@app_views.route('/users/<user_id>', strict_slashes=False, methods=["GET"])
def get_user(user_id):
    """Retrieve user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        return jsonify({"error": "Not found"})

    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """Delete user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        return jsonify({"error": "Not found"})

    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', strict_slashes=False, methods=["POST"])
def create_user():
    """Create a new user"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    if 'email' not in request.json:
        abort(400)
        return jsonify({"error": "Missing email"})
    if 'password' not in request.json:
        abort(400)
        return jsonify({"erro": "Missing password"})

    new_user = User(**request.get_json())
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """Update user info"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    user_attr = request.get_json(silent=True)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        return jsonify({"error": "Not found"})
    for k, v in user_attr.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
