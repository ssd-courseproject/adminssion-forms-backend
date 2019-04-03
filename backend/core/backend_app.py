from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from backend.api import auth, profile

try:
    from backend.config import main_local
except ImportError:
    from backend.config import main as main_local


class FormsBackend(object):

    def __init__(self, flask_app):
        errors = {
            'UserAlreadyExistsError': {
                'message': "A user with that username already exists.",
                'status': 409,
            },
            'ResourceDoesNotExist': {
                'message': "A resource with that ID no longer exists.",
                'status': 410,
                'extra': "Any extra information you want.",
            },
        }

        self.app = flask_app
        self.api = Api(self.app, errors=errors)
        self.db = SQLAlchemy(self.app)
        self.jwt = JWTManager(self.app)
        self.cors = CORS(self.app)

    def init(self):
        try:
            self.app.config.from_object(main_local.LocalConfig)
        except:
            self.app.config.from_object(main_local.DefaultConfig)

        self.api.add_resource(auth.UserLogin, '/auth/login')
        self.api.add_resource(auth.UserLogout, '/auth/logout')
        self.api.add_resource(auth.TokenRefresh, '/auth/refresh')
        self.api.add_resource(profile.UserRegistration, '/profile/register')
        self.api.add_resource(profile.UserProfile, '/profile')

    def run(self, *args, **kwargs):
        self.app.config['PROPAGATE_EXCEPTIONS'] = False
        self.app.run(*args, **kwargs)
