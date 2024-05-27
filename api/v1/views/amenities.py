#!/usr/bin/python3
'''
view for amenity objects
'''
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, request, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    ''' retrieve all amenities '''
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)


@app_views.route('/amenities/<id>', methods=['GET'], strict_slashes=False)
def get_amenity(id):
    ''' retrieve amenity by ID '''
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<id>', methods=['DELETE'], strict_slashes=False)
def del_amenity(id):
    ''' deletes amenity by ID '''
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    ''' creates amenity '''
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def upd_amenity(id):
    ''' update an existing amenity '''
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
