# -*- coding: utf-8 -*-
# api  __init__

from flask import Blueprint, redirect, url_for, request, g, jsonify
from flask_login import login_required, current_user
from flask_restful import Api, Resource

rest = Blueprint('rest', __name__)
api = Api(rest)

from . import res

api.add_resource(res.User, '/user')
api.add_resource(res.Rutz, '/ruts')
api.add_resource(res.Rut, '/rut/<int:rutid>')
api.add_resource(res.Clipz, '/clips')
api.add_resource(res.Demandz, '/demands')
api.add_resource(res.Item, '/item/<int:itemid>')
api.add_resource(res.Commentz, '/comments')

@rest.route('/auth/<servername>')
def auth(servername):
    #from ..auth.views import login
    return redirect(url_for('auth.login', server_name=servername))
