from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    get_raw_jwt, create_refresh_token
from flask_restful import Resource, reqparse

from backend.helpers import success_response, fail_response

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', help='Email cannot be blank', trim=True, required=True)
login_parser.add_argument('password', help='Password cannot be blank', trim=True, required=True)


class UserLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        username = data.username
        password = data.password

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        if username != 'inno' or password != 'great':
            return fail_response('Bad username or password', 401)

        return success_response(
            msg='Logged in as {}'.format(username),
            access_token=access_token,
            refresh_token=refresh_token
        )


class UserLogout(Resource):
    @jwt_required
    def post(self):
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
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        return success_response(access_token=access_token)
