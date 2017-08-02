# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#base class for config
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') # for form CRSF
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  #??
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ADMIN = os.environ.get('WEB_ADMIN')  # init set admin

    POST_PER_PAGE = 20
    FOLLOW_PER_PAGE = 50
    COMMENT_PER_PAGE = 20
    DEMAND_PER_PAGE = 50
    TAG_PER_PAGE = 50
    ITEM_IN_PROFILE = 8
    
    FACEBOOK_AUTH_ID = os.environ.get('FB_ID')  
    FACEBOOK_AUTH_SECRET = os.environ.get('FB_SECRET') 
    GOOGLE_AUTH_ID = os.environ.get('G_ID') 
    GOOGLE_AUTH_SECRET = os.environ.get('G_SECRET') 
    TWITTER_AUTH_ID = os.environ.get('TW_ID') 
    TWITTER_AUTH_SECRET = os.environ.get('TW_SECRET') 

    @staticmethod
    def init_app(app):
        pass

#for development
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB_URI') or 'mysql+pymysql://root:psw@localhost/test'

#for test
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URI') or 'mysql+pymysql://root:psw@localhost/test'

#for production 
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_DB_URI')


config = {
    'development':DevelopmentConfig,
    'test':TestConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}
