from flask import Flask
from flask_restful import Api

from app.api import profile

try:
    from app.config import main_local
except ImportError:
    from app.config import main as main_local


class FormsBackend(object):

    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

    def init(self):
        self.app.config.from_object(main_local.Config)

        self.api.add_resource(profile.UserRegistration, '/register')

    def run(self, *args, **kwargs):
        self.app.config['PROPAGATE_EXCEPTIONS'] = False
        self.app.run(*args, **kwargs)


def run_app(*args, **kwargs):
    application = FormsBackend()

    application.init()
    application.run(*args, **kwargs)

    return application


if __name__ == '__main__':
    application = run_app(debug=True)
    app = application.app
