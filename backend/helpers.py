import os

from datetime import datetime
from flask import jsonify

try:
    from backend.config.main_local import LocalConfig as Config
except ImportError:
    from backend.config.main import Config


def success_response(msg=None, **kwargs):
    return generic_response(status='success', msg=msg, **kwargs)


def fail_response(msg=None, code=None, **kwargs):
    return generic_response(status='fail', msg=msg, code=code, **kwargs)


def generic_response(status, msg=None, code=None, **kwargs):
    if '_data' in kwargs and isinstance(kwargs.get('_data'), dict):
        data = kwargs.pop('_data')
        kwargs = {**kwargs, **data}

    data = {'status': status, 'data': kwargs}
    if msg is not None:
        data['message'] = [msg]

    response = jsonify(data)
    if code is not None:
        response.status_code = code

    return response


def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)


def get_public_path(subpath):
    return os.path.abspath(Config.STATIC_FOLDER + '/' + subpath)


def write_public_file(path, content):
    with open(get_public_path(path), 'w+') as f:
        f.write(content)
