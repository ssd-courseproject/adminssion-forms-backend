import os

from flask import Flask
from backend.core.backend_app import FormsBackend
from backend.helpers import write_public_file

flask_app = Flask(__name__,
                  static_url_path='',
                  static_folder='web/static',
                  template_folder='web/templates')


def init_app():
    app = FormsBackend(flask_app)
    app.init()

    return app


application = init_app()


def extend_app():
    from backend.core.extensions import application_extend
    from backend.core.spec import application_add_spec

    application_extend()
    application_add_spec()


def write_spec():
    from backend.core.spec import generate_spec

    write_public_file("spec.json", generate_spec())


extend_app()
write_spec()

if __name__ == '__main__':
    os.chdir('..')  # go to project root
