from flask import Flask

from backend.config.main import SPEC_FILENAME
from backend.core.backend_app import FormsBackend
from backend.helpers import write_public_file

try:
    from backend.config.main_local import LocalConfig as Config
except ImportError:
    from backend.config.main import Config

flask_app = Flask(__name__, static_url_path=Config.STATIC_URL_PATH, static_folder=Config.STATIC_FOLDER)
application = FormsBackend(flask_app)


def init_app():
    application.init()


def extend_app():
    from backend.core.extensions import application_extend
    from backend.core.spec import application_add_spec

    application_extend(application)
    application_add_spec(application)


def write_spec():
    from backend.core.spec import generate_spec

    write_public_file(SPEC_FILENAME, generate_spec(application))


def get_application():
    return application


init_app()
extend_app()
write_spec()
