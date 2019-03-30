from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from backend.api import auth, profile
from backend.config.main import OPENAPI_VERSION, API_VERSION_NUMBER, APP_NAME
from backend.core.errors import error_descriptions

try:
    from backend.config.main_local import LocalConfig as Config
except ImportError:
    from backend.config.main import Config


class FormsBackend(object):

    def __init__(self, flask_app):
        self.app = flask_app
        self.api = Api(self.app, errors=error_descriptions)
        self.db = SQLAlchemy(self.app)
        self.jwt = JWTManager(self.app)
        self.cors = CORS(self.app)
        self.ma = Marshmallow(self.app)
        self.spec = APISpec(
            title=APP_NAME,
            version=API_VERSION_NUMBER,
            openapi_version=OPENAPI_VERSION,
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )

    def init(self):
        self.app.config.from_object(Config)

        self.api.add_resource(auth.UserLogin, '/auth/login')
        self.api.add_resource(auth.UserLogout, '/auth/logout')
        self.api.add_resource(auth.TokenRefresh, '/auth/refresh')
        self.api.add_resource(profile.UserRegistration, '/profile/register')
        self.api.add_resource(profile.UserProfile, '/profile')

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)
