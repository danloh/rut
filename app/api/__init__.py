# -*- coding: utf-8 -*-
# api  __init__

from flask import Blueprint, current_app
from flask_sqlalchemy import get_debug_queries
from flask_httpauth import HTTPBasicAuth
from .. import db

rest = Blueprint('rest', __name__)
auth = HTTPBasicAuth()

PER_PAGE = 20 # for pagination except items in rut--42

@rest.after_request
def after_request(response):
    #response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    for query in get_debug_queries():
        if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration, query.context))
    return response

from . import authen, errors, rut, item, clip, review, demand, comment, circle, tag, user

# #get request params
# userid = request.args.get('userid', '')
# action = request.args.get('action', '') 
# demandid = request.args.get('demandid', '')
# itemid = request.args.get('itemid', '')
# tagid = request.args.get('tagid', '')