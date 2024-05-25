#!/usr/bin/python3
'''
Routes for the blueprint
'''

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"users": User,
           "places": Place,
           "states": State,
           "cities": City,
           "amenities": Amenity,
           "reviews": Review}


# define route /status
@app_views.route('/status', methods=['GET'])
def status():
    ''' returns status '''
    return jsonify({"status": "OK"})


# define route /stats
@app_views.route('/stats', methods=['GET'])
def stats():
    ''' retrieves the number of each objects by type '''
    stats_dict = {}
    for cls in classes:
        stats_dict[cls] = storage.count(classes[cls])
    # stats_dict = {"states": storage.count(State)} test dummy
    return jsonify(stats_dict)
