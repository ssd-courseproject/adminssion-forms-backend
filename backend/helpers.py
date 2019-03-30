from flask import jsonify


def success_response(msg=None, **kwargs):
    return generic_response(status='success', msg=msg, **kwargs)


def fail_response(msg=None, code=None, **kwargs):
    return generic_response(status='fail', msg=msg, code=code, **kwargs)


def generic_response(status, msg, code=None, **kwargs):
    data = {'status': status, 'data': kwargs}
    if msg is not None:
        data['message'] = msg

    response = jsonify(data)
    if code is not None:
        response.status_code = code

    return response


def write_public_file(path, content):
    with open('public/' + path, 'w+') as f:
        f.write(content)
