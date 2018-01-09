# -*- coding: utf-8 -*-
# register, log in,  etc.

import random
import string
from flask import request, g, jsonify, abort
from ..models import *
from ..task.email import send_email
from . import db, rest, auth, PER_PAGE

def random_code():
    population = string.ascii_letters + string.digits
    s = ''.join(random.sample(population, 9))
    while Users.query.filter_by(recode=s).first():
        s = ''.join(random.sample(population, 9))
    else:
        return s

@rest.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email','').strip()
    if username is None or password is None:
        abort(400) # missing arguments
    if Users.query.filter_by(name = username).first() is not None:
        abort(400) # existing user
    incode = request.json.get('incode','')
    recode = random_code()
    user = Users(
        name = username,
        email = email,
        auth_server = "Registered",
        auth_social_id = "00001",
        incode = incode,
        recode = recode
    )
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    if email:
        token = user.generate_confirmation_token().replace('.', '@')
        url= 'localhost:8080/confirm/%s' %token
        send_email(user.email, 'Confirm Your Account',
                    'email/confirm', name=user.name, url=url)
    # log in once register successfully
    auth_token = user.generate_auth_token()
    return jsonify({
        'username': user.name, 
        'userid': user.id, 
        'token': auth_token.decode('ascii') 
    })

@rest.route('/editprofile', methods = ['POST'])
@auth.login_required
def edit_profile():
    user = g.user
    user.nickname = request.json.get('nickname','').strip()
    user.location = request.json.get('location','').strip()
    user.avatar = request.json.get('avatarUrl','').strip()
    user.about_me = request.json.get('about','').strip()
    user.links = request.json.get('url','').strip()
    db.session.add(user)
    db.session.commit()
    return jsonify('Your Profile Updated')

# check if name / email duplicated when regsiter
@rest.route('/checkname/<username>')
def checkname(username=None):
    if username and Users.query.filter_by(name=username).first() is None:
        return jsonify(1)
    return jsonify(0)
@rest.route('/checkemail/<email>')
def checkemail(email=None):
    if email and Users.query.filter_by(email=email).first() is None:
        return jsonify(1)
    return jsonify(0)

@rest.route('/confirm/<token>')
@auth.login_required
def confirm(token):
    user = g.user
    token = token.replace('@', '.')
    if user.confirmed:
        return jsonify('You have confirmed your account. Thanks!')
    if user.confirm(token):
        db.session.commit()
        return jsonify('You have confirmed your account. Thanks!')
    else:
        return jsonify('The confirmation link is invalid or has expired.')

@rest.route('/confirm')
@auth.login_required
def resend_confirmation():
    user= g.user
    token = user.generate_confirmation_token().replace('.', '@')
    url= 'localhost:8080/confirm/%s' %token
    send_email(user.email, 'Confirm Your Account',
               'email/confirm', name=user.name, url=url)
    return jsonify('A new confirmation email has been sent to you by email.')

@rest.route('/changepassword', methods=['GET', 'POST'])
@auth.login_required
def change_password():
    user = g.user
    old_psw = request.json.get('oldpsw')
    new_psw = request.json.get('newpsw')
    if user.verify_password(old_psw):
        user.password = new_psw
        db.session.add(user)
        db.session.commit()
        return jsonify('Your password Changed, Please login again.')
    else:
        return jsonify('Invalid password.')

@rest.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    email = request.json.get('email')
    username = request.json.get('username')
    user = Users.query.filter_by(email=email, name=username).first()
    if user:
        token = user.generate_reset_token().replace('.', '@')
        url= 'localhost:8080/reset/%s' % token
        send_email(
            user.email, 
            'Reset Your Password',
            'email/reset_password',
            name=user.name, url=url,
            next=request.args.get('next')
        )
        return jsonify('An email with instructions to reset your password has been '
            'sent to you.')
    else:
        return jsonify('Invalid username or email.')

@rest.route('/reset/<string:token>', methods=['GET', 'POST'])
def password_reset(token):
    token = token.replace('@', '.')
    new_psw = request.json.get('newpsw')
    if Users.reset_password(token, new_psw):
        db.session.commit()
        return jsonify('Your password updated, Please login again.')
    else:
        return jsonify('Something wrong, Try Again')

@auth.verify_password
def verify_password(username_or_token, password):
    if request.path == "/api/login":
        user = Users.query.filter_by(name=username_or_token).first()
        if not user or not user.verify_password(password):
            abort(401)
    else:
        user = Users.verify_auth_token(username_or_token)
        if not user:
            abort(401)
    g.user = user
    return True

@auth.error_handler
def auth_error():
    return error_response(401, 'Unauthorized Access')

@rest.route('/login')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({
        'token': token.decode('ascii'),
        'userid': g.user.id
    })