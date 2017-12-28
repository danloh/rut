# -*- coding: utf-8 -*-
# to be re-work

from flask import g, render_template, redirect, request, session, url_for, flash,\
                  current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_oauthlib.client import OAuthException
from config import Config as C
from . import auth
from .. import db, oauth, login_manager
from ..models import Users, Posts, Comments, Reviews, Clips, Messages, Dialog, Events 
from ..safeurl import is_safe_url, get_redirect_target

google = oauth.remote_app(
	'google',
	consumer_key=C.GOOGLE_AUTH_ID,
	consumer_secret=C.GOOGLE_AUTH_SECRET,
	request_token_params={'scope': 'email'},
	base_url='https://www.googleapis.com/oauth2/v1/',
	request_token_url=None,
	access_token_method='POST',
	access_token_url='https://accounts.google.com/o/oauth2/token',
	authorize_url='https://accounts.google.com/o/oauth2/auth',
)

facebook = oauth.remote_app(
	'facebook',
	consumer_key=C.FACEBOOK_AUTH_ID,
	consumer_secret=C.FACEBOOK_AUTH_SECRET,
	request_token_params={'scope': 'email'},
	base_url='https://graph.facebook.com',
	request_token_url=None,
	access_token_url='/oauth/access_token',
	access_token_method='GET',
	authorize_url='https://www.facebook.com/dialog/oauth'
)

twitter = oauth.remote_app(
    'twitter',
    consumer_key=C.TWITTER_AUTH_ID,
    consumer_secret=C.TWITTER_AUTH_SECRET,
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize'
)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@auth.before_app_request
def before_request():
    g.user = current_user

def create_user(me, auth_server_name):  
    if auth_server_name == 'Facebook':
        avatar_url = me.data['picture']['data']['url']
    elif auth_server_name == 'Google':
        avatar_url = me.data['picture']
    else:
        pass
    
    new_user = Users(
        auth_server=auth_server_name, 
        auth_social_id=me.data['id'],
        name=me.data['name'],
        email=me.data['email'],
        avatar=avatar_url,
        nickname = me.data['email'].split('@')[0]
    )  

    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True)
    return new_user

def set_user(server_name, me):
    user = Users.query.filter_by(
        auth_server=server_name, 
        auth_social_id=me.data['id']
    ).first()
    if user is None:
        user = create_user(me, server_name)
        return redirect(url_for('main.edit_profile'))  #note!!

    login_user(user, remember=True)
    next_url = session.pop('next',None)
    return redirect(next_url)  #note!!


def set_tw_user(server_name,resp):
    auth_social_id = resp['user_id']
    name = resp['screen_name']
    email = resp.get('email')

    user = Users.query.filter_by(
        auth_server=server_name, 
        auth_social_id=auth_social_id
    ).first()
    if user is None:
        avatar_url_tw = 'https://twitter.com/%s/profile_image?size=original' % name
        new_user = Users(
            auth_server=server_name, 
            auth_social_id=auth_social_id,
            name=name,
            email=email,
            avatar=avatar_url_tw
        )  
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        #return redirect(url_for('main.edit_profile'))
        g.user = current_user
        user_dict = new_user.to_dict()
        return jsonify(user_dict)

    login_user(user, remember=True)
    next_url = session.pop('next',None)
    #return redirect(next_url)
    user_dict = user.to_dict()
    return jsonify(user_dict)

@auth.route('/connect')
def connect():
    next_c = get_redirect_target()
    session['next'] = next_c
    return None #render_template('connect.html') 

@auth.route('/login/<string:server_name>')
def login(server_name):
    next_c = get_redirect_target()
    session.setdefault('next',next_c)

    '''route to different oauth server'''
    #Google
    if server_name == "Google":
        return google.authorize(
                 callback=url_for('auth.g_authorized', _external=True)
               )

    #Facebook
    elif server_name == "Facebook":
        callback = url_for(
            'auth.facebook_authorized',
            next = get_redirect_target(),
            _external=True
        )
        return facebook.authorize(callback=callback)
    #Twitter
    elif server_name == "Twitter":
        callback_url = url_for(
                        'auth.twitter_authorized', 
                        next = get_redirect_target()
                        )    
        return twitter.authorize(callback=callback_url)   
    
#Facebook
@auth.route('/login/facebook_authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        flash( 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
        )
        next_url = get_redirect_target() or url_for('main.index')
        return redirect(next_url)
    if isinstance(resp, OAuthException):
        flash( 'Access denied: %s' % resp.message)
        next_url = get_redirect_target() or url_for('main.index')
        return redirect(next_url)

    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get(
        '/me/?fields=email,name,id,picture.height(200).width(200)'
    )
    return set_user('Facebook', me)

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
#Facebook end

#Google
@auth.route('/login/g_authorized')
def g_authorized():
    resp = google.authorized_response()
    if resp is None:
        flash( 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
        )
        next_url = get_redirect_target() or url_for('main.index')
        return redirect(next_url)

    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return set_user('Google', me)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
#Google end

#Twitter    
@auth.route('/login/twitter_authorized')
def twitter_authorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
        next_url = get_redirect_target() or url_for('main.index')
        return redirect(next_url)
    
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    return set_tw_user('Twitter', resp)   

@twitter.tokengetter
def get_twitter_token():
    return session.get('twitter_token')   
#Twitter end


@auth.route('/logout')
def logout():
    logout_user()
    return None #redirect(url_for('main.index'))  # note!!!