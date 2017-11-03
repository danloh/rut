# -*- coding: utf-8 -*-
# api  __init__

from flask import Blueprint
from flask_restful import Api, Resource

rest = Blueprint('rest', __name__)
api = Api(rest)

from . import res

api.add_resource(res.User, '/user')
api.add_resource(res.Ruts, '/ruts')
api.add_resource(res.Rut, '/rut/<int:rutid>')
api.add_resource(res.Clipz, '/clips')
