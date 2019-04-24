from flask.json import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from passlib.hash import argon2
from validate_email import validate_email
from webargs.flaskparser import use_args

from backend.core.schema import RegistrationSchema, UsersSchema, CandidatesDocumentsSchema, CandidatesInfoSchema, \
    CandidatesStatusSchema
from backend.helpers import success_response, fail_response, generic_response
from server import application

USERS_PER_PAGE = 5


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
    def get(self, u_id):
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

        user = application.orm.get_user(u_id)
        documents = application.orm.get_document(u_id)
        info = application.orm.get_info(u_id)
        status = application.orm.get_status(u_id)
        user_schema = UsersSchema()
        docs_schema = CandidatesDocumentsSchema()
        info_schema = CandidatesInfoSchema()
        status_schema = CandidatesStatusSchema()

        profile = dict()
        profile.update({'user': user_schema.dump(user)})
        profile.update({'document': docs_schema.dump(documents)})
        profile.update({'status': info_schema.dump(status)})
        profile.update({'info': status_schema.dump(info)})
        return jsonify(profile)

    @jwt_required
    def put(self):
        """
        ---
        summary: Profile update
        description: Updates user profile data
        """
        return success_response()


class UsersList(Resource):
    def get(self, page=1):
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
        users = application.orm.get_users(page_num=page, num_of_users=USERS_PER_PAGE)
        if users is None:
            return fail_response("Some problems with users retrieving", code=404)
        user_schema = UsersSchema(many=True)
        res = user_schema.dump(users)

        return jsonify(res.data)
