class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DefaultConfig(Config):
    SECRET_KEY = 'some-secret-string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    JWT_SECRET_KEY = 'jwt-secret-string'


API_VERSION_NUMBER = '0.1'
API_VERSION_LABEL = 'v1'
