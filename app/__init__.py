# -*- coding: utf-8 -*-
# app __init__.py

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_mail import Mail
from flask_cors import CORS

from config import config 
 
db = SQLAlchemy()
cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT':60*10
    })
mail = Mail()
cors = CORS()

def create_app(config_name):
    app = Flask(__name__)
    #load config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #load extension
    db.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    cors.init_app(app)

    #load blueprints
    from .api import rest as rest_blueprint
    app.register_blueprint(rest_blueprint, url_prefix='/api')

    from .bot import bot as bot_blueprint
    app.register_blueprint(bot_blueprint)
    
    return app

from . import models