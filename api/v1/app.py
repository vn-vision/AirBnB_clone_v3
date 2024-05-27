#!/usr/bin/python3
'''
AirBnB API: app
'''

from flask import Flask, jsonify
import os
from models import storage
from api.v1.views import app_views

# create an instance of Flask
app = Flask(__name__)

# register blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def trdown(exception):
    ''' clean up after use, close access to storage '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    ''' error 404 '''
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    # get the host and port from environment with default values
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
