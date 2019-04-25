from flask import jsonify

from backend.core.backend_app import FormsBackend


def application_extend(application: FormsBackend):
    from backend.core.models import Users
    from backend.core.enums import UsersRole
    from flask_jwt_extended import get_current_user

    @application.jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']

        model = application.orm.get_token_by_jti(jti)
        if not model:
            return False
        if model.revoked:
            return True

        return False

    @application.jwt.user_loader_callback_loader
    def fetch_user(identity) -> Users:
        print(identity)
        user_auth = application.orm.get_user_auth_by_email(identity)
        print(user_auth)

        return user_auth.user

    @application.app.before_request
    def log_request():
        from flask import request

        user: Users = get_current_user()

        if user is not None:
            if user.role == UsersRole.MANAGER or user.role == UsersRole.STAFF:
                path = request.url
                data = request.get_json()

                application.orm.add_log(user.id, user.role, path, data)

    @application.app.errorhandler(422)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])

        msg_list = []
        if isinstance(messages, list):
            msg_list = messages
        else:
            for value in messages.values():
                msg_list += value

        res = jsonify({'message': msg_list})
        if headers:
            return res, err.code, headers
        else:
            return res, err.code
