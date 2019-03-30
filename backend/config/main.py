class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DefaultConfig(Config):
    SECRET_KEY = 'some-secret-string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    JWT_SECRET_KEY = 'jwt-secret-string'


APP_NAME = 'Admission Portal'

API_VERSION_NUMBER = '0.0.2'
API_VERSION_LABEL = 'v1'

OPENAPI_VERSION = '3.0.2'
