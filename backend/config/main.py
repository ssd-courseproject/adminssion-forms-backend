class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = False

    SECRET_KEY = 'some-secret-string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    JWT_SECRET_KEY = 'jwt-secret-string'

    STATIC_URL_PATH = '/static'
    STATIC_FOLDER = 'public'


API_VERSION_NUMBER = '0.0.4'
API_VERSION_LABEL = 'v1'

OPENAPI_META = """
    openapi: 3.0.2
    info:
        description: 'IU admission portal backend API (prototype)'
        title: 'Admission Portal'
        version: {}
    tags:
        - name: Auth
        - name: Profile
        - name: Tests
        - name: Submissions
    servers:
        - url: /
          description: Current server
""".format(API_VERSION_NUMBER)

SPEC_FILENAME = 'spec.json'
