from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from backend.helpers import success_response

register_parser = reqparse.RequestParser()
register_parser.add_argument('name', help='Name cannot be blank', trim=True, required=True)
register_parser.add_argument('surname', help='Surname cannot be blank', trim=True, required=True)
register_parser.add_argument('email', help='Email cannot be blank', trim=True, required=True)
register_parser.add_argument('password', help='Password cannot be blank', trim=True, required=True)


class UserRegistration(Resource):
    def post(self):
        """
        ---
        summary: Registration
        description: Creates new user profile
        """
        data = register_parser.parse_args()
        return {'message': 'User registration'}


class UserProfile(Resource):
    @jwt_required
    def get(self):
        """
        ---
        summary: Profile info
        description: Gives all information about current user's profile
        """
        current_user = get_jwt_identity()

        return success_response(
            email=current_user,
            name='Sergey',
            surname='Malyutkin',
            natinality='RU',
            gender=1,
            date_of_birth='1970-01-01',
        )

    @jwt_required
    def put(self):
        """
        ---
        summary: Profile update
        description: Updates user profile data
        """
        return success_response()
