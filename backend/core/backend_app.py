from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
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
    routes = {
        'auth': {
            'login': auth.UserLogin,
            'logout': auth.UserLogout,
            'refresh': auth.TokenRefresh,
        },
        'profile': {
            '': profile.UserProfile,
            'register': profile.UserRegistration,
        }
    }

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

        self._add_routes(self.routes)

    def _add_routes(self, routes, prefix=''):
        for path in routes:
            p_path = (prefix + '/' + path.strip('/')).rstrip('/')
            route = routes[path]

            if isinstance(route, dict):
                self._add_routes(route, prefix=p_path)
            elif issubclass(route, Resource):
                self._add_resource(route, path=p_path)
            else:
                raise Exception("Unknown route type")

    def _add_resource(self, resource: Resource.__class__, path: str):
        self.api.add_resource(resource, path)

        self._add_resource_spec(resource)

    def _add_resource_spec(self, resource: Resource.__class__):
        """
        Register resource
        """
        method_name = resource.__name__.lower()
        method_view = self.app.view_functions[method_name]

        with self.app.test_request_context():
            # self.spec.add_path(resource=resource, api=application.api)
            self.spec.path(view=method_view)

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)
