#!/usr/bin/python3
'''
Routes for the blueprint
'''

from api.v1.views import app_views
from flask import jsonify


# define route /status
@app_views.route('/status', methods=['GET'])
def status():
    ''' returns status '''
    return jsonify({"status": "OK"})
