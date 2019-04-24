error_descriptions = {
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
    },
    'InsufficientRights': {
        'message': ["You have insufficient rights fot this action"],
        'status': 403
    }
}


class InsufficientRights(Exception):
    pass


class UserDoesNotExist(Exception):
    pass
