from flask import jsonify


def success_response(msg=None, **kwargs):
    return generic_response(status='success', msg=msg, **kwargs)


def fail_response(msg=None, code=None, **kwargs):
    return generic_response(status='fail', msg=msg, code=code, **kwargs)


def generic_response(status, msg, code=None, **kwargs):
    r = {'status': status, 'data': kwargs}

    if msg is not None:
        r['message'] = msg

    if code is not None:
        return jsonify(r)
    else:
        return r, code
