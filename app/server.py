from flask import Flask, jsonify
from app.core.backend_app import FormsBackend


flask_app = Flask(__name__)


def run_app(*args, **kwargs):
    application = FormsBackend(flask_app)

    application.init()
    application.run(*args, **kwargs)

    return application


application = run_app(debug=True)

import app.core.extensions
