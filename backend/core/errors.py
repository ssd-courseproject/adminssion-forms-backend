error_descriptions = {
    'NoAuthorizationError': {
        'message': ["Authorization token not provided."],
        'status': 401,
    },
    'InsufficientRights': {
        'message': ["You have insufficient rights fot this action"],
        'status': 403
    },
    'MethodNotAllowed': {
        'message': ["The method is not allowed for the requested URL."],
        'status': 405,
    },
    'ResourceDoesNotExist': {
        'message': ["A resource with that ID no longer exists."],
        'status': 410,
    },
    'ExpiredSignatureError': {
        'message': ["Your token is expired."],
        'status': 419,
    },
    'RevokedTokenError': {
        'message': ["Your token has been revoked."],
        'status': 420,
    },
}


class InsufficientRights(Exception):
    pass


class UserDoesNotExist(Exception):
    pass
