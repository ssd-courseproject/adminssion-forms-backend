from flask import Flask
from backend.core.backend_app import FormsBackend

flask_app = Flask(__name__)


def run_app(*args, **kwargs):
    application = FormsBackend(flask_app)

    application.init()
    application.run(*args, **kwargs)

    return application


application = run_app(debug=True)

from backend.core.extensions import application_extend
application_extend()
