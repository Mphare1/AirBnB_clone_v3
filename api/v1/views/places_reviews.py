#!/usr/bin/python3
"""A view for reviews of places"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=["GET"])
def get_reviews(place_id):
    """Retrieve reviews for a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
        return jsonify({"error": "Not found"})
    reviews = storage.all(Review)
    review_list = []

    for k, v in reviews.items():
        if v.place_id == place_id:
            review_list.append(v.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """Retrieve a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
        return jsonify({"error": "Not found"})

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """Delete a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
        return jsonify({"error": "Not found"})
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """Create a review"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    if 'user_id' not in request.json:
        abort(400)
        return jsonify({"error": "Missing user_id"})
    if 'text' not in request.json:
        abort(400)
        return jsonify({"error": "Missing text"})

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
        return jsonify({"error": "Not found"})
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
        return jsonify({"error": "Not found"})

    new_review = Review(**request.get_json())
    setattr(new_review, 'place_id', place_id)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=["PUT"])
def update_review(review_id):
    """Update a review"""
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    review_atr = request.get_json(silent=True)
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
        return jsonify({"error": "Not found"})

    for k, v in review_atr.items():
        if k not in ["id", "created_at", "updated_at", "user_id", "place_id"]:
            setattr(review, k, v)

    review.save()
    return jsonify(review.to_dict())
