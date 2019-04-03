from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    get_raw_jwt, create_refresh_token
from flask_restful import Resource, reqparse

from backend.helpers import fail_response,success_response
from backend.core import models

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

    @jwt_required
    def get(self, test_id):
        if not Utils.is_test_exist(test_id):
            return fail_response(msg="Test is not exist", code=404)
        models.


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


class Utils:
    @staticmethod
    def is_test_exist(test_id):
        if test_id == 1:
            return True
        else:
            return False
