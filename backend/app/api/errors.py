# -*- coding: utf-8 -*-

from flask import json
from werkzeug.wrappers import Response

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
