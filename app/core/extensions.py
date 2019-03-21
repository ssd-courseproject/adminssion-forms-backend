from app.server import application

print(123)

@application.jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return True
    # jti = decrypted_token['jti']
    # return RevokedTokenModel.is_jti_blacklisted(jti)
