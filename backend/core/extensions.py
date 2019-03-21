from backend.server import application


def application_extend():

    @application.jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return False
        # jti = decrypted_token['jti']
        # return RevokedTokenModel.is_jti_blacklisted(jti)
