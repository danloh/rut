# -*- coding: utf-8 -*-
# app __init__.py

from flask import Flask 
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

from flask_oauthlib.client import OAuth
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown

from config import config 

bootstrap = Bootstrap()  # to be init_ed later
moment = Moment()
pagedown = PageDown() 
db = SQLAlchemy()
cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT':60*10
    })

oauth = OAuth()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.connect'

def create_app(config_name):
    app = Flask(__name__)
    #load config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #load extension
    bootstrap.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    db.init_app(app)
    cache.init_app(app)

    oauth.init_app(app)
    login_manager.init_app(app)

    #load blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .bot import bot as bot_blueprint
    app.register_blueprint(bot_blueprint)
    
    return app

from . import models