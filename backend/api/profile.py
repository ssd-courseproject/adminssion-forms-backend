from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from webargs.flaskparser import use_args

from backend.core.schema import RegistrationSchema
from backend.helpers import success_response

register_parser = reqparse.RequestParser()
register_parser.add_argument('name', help='Name cannot be blank', trim=True, required=True)
register_parser.add_argument('surname', help='Surname cannot be blank', trim=True, required=True)
register_parser.add_argument('email', help='Email cannot be blank', trim=True, required=True)
register_parser.add_argument('password', help='Password cannot be blank', trim=True, required=True)


class UserRegistration(Resource):
    @use_args(RegistrationSchema)
    def post(self, args):
        """
        ---
        summary: Registration
        description: Creates new user profile
        requestBody:
          required: true
          content:
            application/json:
              schema: RegistrationSchema
              example:
                email: super@innopolis.ru
                password: 123456
                name: Super
                surname: Innopolis
        responses:
          201:
            description: OK
          406:
            description: User already exists
            content:
              application/json:
                schema: ErrorSchema
                example:
                  message: [A user with that email already exists.]
        """
        return jsonify(), 201


class UserProfile(Resource):
    @jwt_required
    def get(self):
        """
        ---
        summary: Profile info
        description: All information about current user's profile
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: ProfileInfoSchema
                example:
                    user:
                      first_name:
                      last_name:
                      role:
                    authentication:
                      email:
                    info:
                      skype:
                      subscription_email:
                      gender:
                      date_of_birth:
                      phone:
                      nationality:
                    documents:
                      cv:
                      passport:
                      transcript:
                      project_description:
                      photo:
                      motivation_letter:
                      letter_of_recommendation:
                    status:
                      status:
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
