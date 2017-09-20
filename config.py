# -*- coding: utf-8 -*-

import os
#basedir = os.path.abspath(os.path.dirname(__file__))

#base class for config
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') # for form CRSF
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  #?? it is said not reliable as thought
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    SLOW_DB_QUERY_TIME=0.25

    POST_PER_PAGE = 20
    FOLLOW_PER_PAGE = 50
    COMMENT_PER_PAGE = 20
    DEMAND_PER_PAGE = 50
    TAG_PER_PAGE = 50
    ITEM_IN_PROFILE = 8

    ADMIN = os.environ.get('WEB_ADMIN')  # init set admin
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

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        #log to file
        import logging
        log_file = os.path.join(os.getcwd(),'log/app_run.log')
        file_handler = logging.FileHandler(log_file, encoding='UTF-8')
        file_handler.setLevel(logging.DEBUG)
        logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
        file_handler.setFormatter(logging_format)
        app.logger.addHandler(file_handler)

#config dict 
config = {
    'development':DevelopmentConfig,
    'test':TestConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}
