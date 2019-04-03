from flask import jsonify

from backend.core.backend_app import FormsBackend


def application_extend(application: FormsBackend):
    @application.jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return False
        # jti = decrypted_token['jti']
        # return RevokedTokenModel.is_jti_blacklisted(jti)

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
