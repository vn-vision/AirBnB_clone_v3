#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieve all Place objects for a given City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object by its ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object by its ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new Place object for a given City."""
    city = storage.get(City, city_id)
    if not city:
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

    if 'name' not in json_data:
        abort(400, description="Missing name")

    json_data['city_id'] = city_id
    new_place = Place(**json_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object by its ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")

    ignore_keys = {'id', 'user_id', 'city_id', 'created_at', 'updated_at'}
    for key, value in json_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on provided JSON data."""
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")

    states = json_data.get('states', [])
    cities = json_data.get('cities', [])
    amenities = json_data.get('amenities', [])

    places = []

    # Retrieve places based on states
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                places.extend(city.places)

    # Retrieve places based on cities
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places.extend(city.places)

    # Filter places based on amenities
    if amenities:
        filtered_places = []
        for place in places:
            place_amenities = [amenity.id for amenity in place.amenities]
            if all(amenity_id in place_amenities for amenity_id in amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])
