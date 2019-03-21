from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort, reqparse

from app.helpers import success_response

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
        current_user = get_jwt_identity()

        return success_response(
            username=current_user,
            name='Sergey',
            surname='Malyutkin',
            natinality='RU',
            gender=1,
            date_of_birth='1970-01-01',
            email='inno@iinopolis.ru'
        )
