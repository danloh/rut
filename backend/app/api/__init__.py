# -*- coding: utf-8 -*-
# api  __init__

from flask import Blueprint, redirect, url_for, request, g, jsonify
from flask_login import login_required, current_user
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth

rest = Blueprint('rest', __name__)
api = Api(rest)

auth = HTTPBasicAuth()

from . import res

api.add_resource(res.User, '/user')
api.add_resource(res.Rutz, '/ruts')
api.add_resource(res.Rut, '/rut/<int:rutid>')
api.add_resource(res.Clipz, '/clips')
api.add_resource(res.Demandz, '/demands')
api.add_resource(res.Item, '/item/<int:itemid>')
api.add_resource(res.Commentz, '/comments')

# for user authentication
@rest.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if Users.query.filter_by(name = username).first() is not None:
        abort(400) # existing user
    user = Users(name = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.name, 'userid': user.id })

@auth.verify_password
def verify_password(username_or_token, password):
    if request.path == "/api/login":
        user = Users.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    else:
        user = Users.verify_auth_token(username_or_token)
        if not user:
            return False    
    g.user = user   
    return True

@rest.route('/login')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify(token)

# @rest.route('/auth/<servername>')
# def auth(servername):
#     #from ..auth.views import login
#     return redirect(url_for('auth.login', server_name=servername))
