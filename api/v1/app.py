#!/usr/bin/python3
'''
AirBnB API: app
'''

from flask import Flask
import os
import json
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


def create_404_json():
    ''' Create a JSON file with 404 error content '''
    error_page = {
        "error": "not found"
    }
    with open('404.json', 'w') as json_file:
        json.dump(error_page, json_file, indent=2)
    print('404.json has been saved!')


if __name__ == "__main__":
    # get the host and port from environment with default values
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
