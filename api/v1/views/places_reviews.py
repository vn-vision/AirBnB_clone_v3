#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieve all Review objects for a given Place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object by its ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object by its ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new Review object for a given Place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    
    if 'user_id' not in json_data:
        abort(400, description="Missing user_id")
    
    user_id = json_data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    
    if 'text' not in json_data:
        abort(400, description="Missing text")
    
    json_data['place_id'] = place_id
    new_review = Review(**json_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object by its ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    
    ignore_keys = {'id', 'user_id', 'place_id', 'created_at', 'updated_at'}
    for key, value in json_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    
    review.save()
    return jsonify(review.to_dict()), 200
