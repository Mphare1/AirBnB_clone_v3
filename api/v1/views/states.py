#!/usr/bin/python3
"""states"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route("/states", strict_slashes=False, methods=["GET"])
def states():
    """retrievs the list of all states objects"""
    all_states = storage.all(State)
    states_list = []

    for k, v in all_states.items():
        states_list.append(v.to_dict())

    return jsonify(states_list)

@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id):
    """Get a state with the id"""
    try:
        state = storage.get(State, state_id)
        return state.to_dict()
    except Exception:
        abort(404)

@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id):
    """Delete state from api call"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
        return jsonify({"error": "Not found"})
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """Create a state object"""

    if not request.json:
        abort(400)
        return jsonify({'error': 'Not a JSON'})
    if 'name' not in request.json:
        abort(400)
        return jsonify({'error': 'Missing name'})
    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """update a state object"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    my_json = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

  
    for k, v in my_json.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
