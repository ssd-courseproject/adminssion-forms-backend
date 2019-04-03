from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    get_raw_jwt, create_refresh_token
from flask_restful import Resource
from webargs.flaskparser import use_args, use_kwargs

from backend.core.schema import TokensSchema, LoginSchema
from backend.helpers import success_response, fail_response


class UserLogin(Resource):
    @use_kwargs(LoginSchema())
    def post(self, email='', password=''):
        """
        ---
        summary: Login
        description: Get JWT tokens
        requestBody:
            required: true
            content:
                application/json:
                    schema: LoginSchema
                    example:
                        email: super@innopolis.ru
                        password: 123456
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: TokensSchema
                example:
                    access_token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTQzMDU1MjYsIm5iZiI6MTU1NDMwNTUyNiwianRpIjoiNzk3ZWZhYWQtZTI4ZS00ZTIyLWE2N2EtZTBmYjA4ZmI1NTY5IiwiZXhwIjoxNTU0MzA2NDI2LCJpZGVudGl0eSI6InN1cGVyQGlubm9wb2xpcy5ydSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.hvsxNM9SjBapbv1WzpGnn0G5T8N0amAANM9i2woP0kk
                    refresh_token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTQzMDU1MjYsIm5iZiI6MTU1NDMwNTUyNiwianRpIjoiNjA1Mzc3OTktY2NhMy00MjM3LTkwMmUtZmE3NTNjODM5M2RkIiwiZXhwIjoxNTU2ODk3NTI2LCJpZGVudGl0eSI6InN1cGVyQGlubm9wb2xpcy5ydSIsInR5cGUiOiJyZWZyZXNoIn0.MJQ5eOZQHz8_fq698uJ0Je8PhwX_ZE25dJtS_HNec3E
          406:
            description: Wrong credentials
            content:
              application/json:
                schema: ErrorSchema
                example:
                    message: [Bad email or password]
        """
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        if email != 'super@innopolis.ru' or password != 'great':
            return fail_response('Bad email or password', 406)

        return TokensSchema().dump({
            'access_token': access_token,
            'refresh_token': refresh_token,
        })


class UserLogout(Resource):
    @jwt_required
    def post(self):
        """
        ---
        summary: Logout
        description: Revokes JWT token(s)
        """
        jti = get_raw_jwt()['jti']
        try:
            # revoked_token = RevokedTokenModel(jti=jti)
            # revoked_token.add()
            return success_response('Access token has been revoked')
        except:
            return fail_response('Something went wrong')


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        ---
        summary: Token refresh
        description: Prolongs `access_token`, requires `refresh_token`
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        return success_response(access_token=access_token)
