from flask import jsonify
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    get_raw_jwt, create_refresh_token
from flask_restful import Resource
from webargs.flaskparser import use_args, use_kwargs
from passlib.hash import argon2

from backend.core.enums import TokenType
from backend.core.schema import TokensSchema, LoginSchema
from backend.helpers import success_response, fail_response

from server import application


class UserLogin(Resource):
    @use_kwargs(LoginSchema)
    def post(self, email, password):
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
            description: Invalid credentials
            content:
              application/json:
                schema: ErrorSchema
                example:
                  message: [Bad email or password]
        """
        ORM = application.orm

        user_auth = ORM.get_user_auth_by_email(email=email)
        if not user_auth:
            return fail_response('Bad email or password', code=406)

        if not argon2.verify(password, user_auth.password):
            return fail_response('Bad email or password', 406)

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        ORM.add_token(jti=access_token, token_type=TokenType.ACCESS, user_id=user_auth.id)
        ORM.add_token(jti=refresh_token, token_type=TokenType.REFRESH, user_id=user_auth.id)

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
        description: Revokes JWT token
        responses:
          202:
            description: OK
        """
        jti = get_raw_jwt()['jti']
        try:
            # revoked_token = RevokedTokenModel(jti=jti)
            # revoked_token.add()
            return jsonify(), 202
        except:
            return fail_response('Something went wrong', code=500)


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        ---
        summary: Token refresh
        description: Gives new `access_token`, requires `refresh_token`
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: TokensSchema
                example:
                  access_token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTQzMDU1MjYsIm5iZiI6MTU1NDMwNTUyNiwianRpIjoiNzk3ZWZhYWQtZTI4ZS00ZTIyLWE2N2EtZTBmYjA4ZmI1NTY5IiwiZXhwIjoxNTU0MzA2NDI2LCJpZGVudGl0eSI6InN1cGVyQGlubm9wb2xpcy5ydSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.hvsxNM9SjBapbv1WzpGnn0G5T8N0amAANM9i2woP0kk
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        return TokensSchema().dump({
            'access_token': access_token
        })
