from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    get_raw_jwt, create_refresh_token
from flask_restful import Resource, reqparse

from backend import helpers


class TestList(Resource):  # /test
    @jwt_required
    def post(self):
        pass

    @jwt_required
    def get(self):
        pass


class Test(Resource):  # test/id put get delete
    @jwt_required
    def delete(self, test_id):
        pass

    @jwt_required
    def put(self, test_id):
        pass


class TimerStart(Resource):  # test/id/start post
    @jwt_required
    def post(self, test_id):
        pass


class TimerCheckpoint(Resource):  # test/id/checkpoint post
    @jwt_required
    def post(self, test_id):
        pass


class TimerEnd(Resource):  # test/id/submit post
    @jwt_required
    def post(self, test_id):
        pass


class SubmissionsList(Resource):  # submissions/test_id/list get
    @jwt_required
    def get(self, test_id):
        pass


class Submission(Resource):  # submissions/submission_id get post
    @jwt_required
    def post(self, submission_id):
        pass

    @jwt_required
    def get(self, submission_id):
        pass


