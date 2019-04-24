error_descriptions = {
    'UserAlreadyExistsError': {
        'message': ["A user with that email already exists."],
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': ["A resource with that ID no longer exists."],
        'status': 410,
    },
    'ExpiredSignatureError': {
        'message': ["Your token is expired."],
        'status': 419,
    },
    'NoAuthorizationError': {
        'message': ["Authorization token not provided."],
        'status': 401,
    },
    'MethodNotAllowed': {
        'message': ["The method is not allowed for the requested URL."],
        'status': 405,
    }
}


class UserAlreadyExist(Exception):
    pass


class UserDoesNotExist(Exception):
    pass
