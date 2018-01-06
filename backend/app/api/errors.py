# -*- coding: utf-8 -*-

from flask import json
from werkzeug.wrappers import Response

from . import rest

def error_response(status_code, message=None):
    payload = {'status': status_code}
    if message:
        payload['message'] = message
    response = Response(
        json.dumps(payload),
        status=status_code,
        mimetype='application/json'
    )
    return response

@rest.errorhandler(400)
@rest.errorhandler(401)
@rest.errorhandler(403)
@rest.errorhandler(404)
@rest.errorhandler(418)
@rest.errorhandler(500)
def error_handler(error):
    if hasattr(error, 'name'):
        msg = error.name
        code = error.code
    else:
        msg = error.message
        code = 500
    return error_response(code, message=msg)

#################################################
## just for test
@rest.route('/testerror')
#@auth.login_required
def test_error():
    abort(502)
##################################################