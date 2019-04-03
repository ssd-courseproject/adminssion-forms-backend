from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    get_raw_jwt, create_refresh_token
from flask_restful import Resource, reqparse

from app.helpers import success_response, fail_response




class ActualTest(Resource):
    @jwt_required
    def post(self):
        pass


    @jwt_required
    def get(self):
        pass

    @jwt_required
    def put(self):
        pass


class ArchivedTest(Resource):
    @jwt_required
    def post(self):
        pass

    @jwt_required
    def get(self):
        pass

    @jwt_required
    def put(self):
        pass


class TestAnswers(Resource):
    @jwt_required
    def post(self):
        pass

    @jwt_required
    def get(self):
        pass

    @jwt_required
    def put(self):
        pass


