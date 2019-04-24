from collections import OrderedDict

import yaml
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from backend.config.main import OPENAPI_META
from backend.core.errors import error_descriptions

try:
    from backend.config.main_local import LocalConfig as Config
except ImportError:
    from backend.config.main import Config


class FormsBackend(object):
    orm = None

    def __init__(self, flask_app):
        self.app = flask_app
        self.app.config.from_object(Config)

        self.api = Api(self.app, errors=error_descriptions)
        self.db = SQLAlchemy(self.app)
        self.migrate = Migrate(self.app, self.db)
        self.jwt = JWTManager(self.app)
        self.cors = CORS(self.app)
        self.ma = Marshmallow(self.app)
        self.spec = self._init_api_spec()

    def init(self):
        from backend.core.models import ORM
        self.orm = ORM(self.db)

        self._add_routes(self._get_routes())

    def _get_routes(self):
        from backend.api import auth, profile, test, submission

        return {
            'auth': {
                'login': auth.UserLogin,
                'logout': auth.UserLogout,
                'refresh': auth.TokenRefresh,
            },
            'profile': {
                '': profile.UserProfile,
                'register': profile.UserRegistration,
                'list': {
                    '<int:page>': {
                        '': profile.UsersList
                    },
                }

            },
            'tests': {
                '<int:test_id>': {
                    '': test.TestManagement,
                    'start': test.TestStart,
                    'submissions': test.TestSubmissions,
                },
                'list': test.TestsList,
                'create': test.TestCreation,
            },
            'submissions': {
                '<int:submission_id>': {
                    '': submission.SubmissionsManagement,
                    'checkpoint': submission.SubmissionCheckpoint,
                    'complete': submission.SubmissionComplete,
                },
            }
        }

    def _init_api_spec(self):
        settings = yaml.safe_load(OPENAPI_META)

        title = settings["info"].pop("title")
        spec_version = settings["info"].pop("version")
        openapi_version = settings.pop("openapi")

        spec = APISpec(
            title=title,
            version=spec_version,
            openapi_version=openapi_version,
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
            **settings
        )
        # validate_spec(spec)

        return spec

    def _add_routes(self, routes, prefix='', root_name=None):
        for path in routes:
            s_path = path.strip('/')

            if root_name is not None:
                loc_root = root_name
            elif len(s_path) > 0:
                loc_root = s_path.title()
            else:
                loc_root = None

            p_path = (prefix + '/' + s_path).rstrip('/')
            route = routes[path]

            if isinstance(route, dict):
                self._add_routes(route, prefix=p_path, root_name=loc_root)
            elif issubclass(route, Resource):
                self._add_resource(route, path=p_path, root_name=root_name)
            else:
                raise Exception("Unknown route type")

    def _add_resource(self, resource: Resource.__class__, path: str, root_name: str = None):
        # print(path)
        self.api.add_resource(resource, path)
        self._add_resource_spec(resource, root_name)

    def _add_resource_spec(self, resource: Resource.__class__, root_name: str = None):
        """
        Register resource
        """
        method_name = resource.__name__.lower()
        method_view = self.app.view_functions[method_name]

        with self.app.test_request_context():
            # self.spec.add_path(resource=resource, api=application.api)
            self.spec.path(view=method_view)

            if root_name is not None:
                path = FlaskPlugin().path_helper(view=method_view, operations=OrderedDict())
                spec_path = self.spec._paths[path]

                for op_name in spec_path:
                    if "tags" not in spec_path[op_name]:
                        spec_path[op_name]["tags"] = [root_name]

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)
