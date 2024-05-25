#!/usr/bin/python3
''' this is a package '''
from flask import Blueprint

# blueprint instance
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

if app_views is not None:
    from api.v1.views.index import *