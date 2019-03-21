from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort, reqparse

register_parser = reqparse.RequestParser()
register_parser.add_argument('name', help='Name cannot be blank', trim=True, required=True)
register_parser.add_argument('surname', help='Surname cannot be blank', trim=True, required=True)
register_parser.add_argument('username', help='Username cannot be blank', trim=True, required=True)
register_parser.add_argument('password', help='Password cannot be blank', trim=True, required=True)


class UserRegistration(Resource):
    def post(self):
        data = register_parser.parse_args()
        return {'message': 'User registration'}


class UserProfile(Resource):
    @jwt_required
    def get(self):
        abort(409, message="A user with that username already exists.")
