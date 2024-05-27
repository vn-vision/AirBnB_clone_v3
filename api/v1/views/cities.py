#!/usr/bin/python3
'''
view for city objects
id: represents city ID
state_id: represents the state ID
'''
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    ''' retrieve all cities '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route('/cities/<id>', methods=['GET'], strict_slashes=False)
def get_city(id):
    ''' retrieve city by ID '''
    city = storage.get(City, id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<id>', methods=['DELETE'], strict_slashes=False)
def del_city(id):
    ''' deletes city by ID '''
    city = storage.get(City, id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    ''' creates city '''

    state = storage.get(State, state_id)
    if not state:
        abort(404)


    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")

    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<id>', methods=['PUT'], strict_slashes=False)
def upd_city(id):
    ''' update an existing city '''
    city = storage.get(City, id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
