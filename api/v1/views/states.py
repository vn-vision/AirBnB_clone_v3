#!/usr/bin/python3
'''
view for state objects
'''
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    ''' retrieve all states '''
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def get_state(id):
    ''' retrieve state by ID '''
    state = storage.get(State, id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def del_state(id):
    ''' deletes state by ID '''
    state = storage.get(State, id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    ''' creates state '''
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def upd_state(id):
    ''' update an existing state '''
    state = storage.get(State, id)
    if not state:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
