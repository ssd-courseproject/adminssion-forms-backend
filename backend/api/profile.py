from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from webargs.flaskparser import use_args
from passlib.hash import argon2
from validate_email import validate_email

from backend.core.schema import RegistrationSchema
from backend.helpers import success_response, fail_response, generic_response

from server import application


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
                $ref: '#/components/examples/Registration'
        responses:
          201:
            description: OK
          406:
            description: Invalid data provided
            content:
              application/json:
                schema: ErrorSchema
                example:
                  message: [Invalid email]
          409:
            description: User already exists
            content:
              application/json:
                schema: ErrorSchema
                example:
                  message: [A user with that email already exists.]
        """
        ORM = application.orm

        # if not validate_email(args["email"], check_mx=True, verify=True):
        if not validate_email(args["email"]):
            return fail_response('Invalid email', code=406)

        existing_user = ORM.get_user_auth_by_email(email=args["email"])
        if existing_user:
            return fail_response('User with such email already exists', code=409)

        user = ORM.add_user(first_name=args["name"], last_name=args["surname"])
        ORM.add_candidates_authorization(u_id=user.id, email=args["email"], password=argon2.hash(args["password"]))

        ORM.add_candidates_documents(u_id=user.id)
        ORM.add_candidates_info(candidate_id=user.id)

        return generic_response(201)


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
                    $ref: '#/components/examples/ProfileFull'
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


class UsersList(Resource):
    @jwt_required
    def get(self):
        """
        ---
        summary: Users list
        description: List of all users with pagination, filtering and sorting
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: ProfileInfoSchema
                many: true
                example:
                    - $ref: '#/components/examples/ProfileFull'
                    - $ref: '#/components/examples/ProfileFull'
        """
        current_user = get_jwt_identity()

        return success_response([{
            'email': current_user,
            'name': 'Sergey',
            'surname': 'Malyutkin',
            'natinality': 'RU',
            'gender': 'MALE',
            'date_of_birth': '1970-01-01',
        }])
