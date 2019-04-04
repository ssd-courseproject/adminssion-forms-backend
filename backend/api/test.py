from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    get_raw_jwt, create_refresh_token
from flask_restful import Resource, reqparse
from flask import request, jsonify

from backend.helpers import fail_response, success_response
from backend.core import models


class TestList(Resource):  # /test
    @jwt_required
    def post(self):
        """
        ---
        summary: Test creation
        description: Creates new test
        requestBody:
          required: true
          content:
            application/json:
              schema: TestSchema
        responses:
          201:
            description: OK

          403:
            description: Not authorized
              content:
                application/json:
                    schema: ErrorSchema
                    example:
                        message: [Not allowed for this action]
        """
        return jsonify(), 201

    @jwt_required
    def get(self):
        """
        ---
        summary: Get all tests list
        description: All tests with links on them
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: array
                            items: TestSchema
            403:
                description: Not authorized
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Not allowed for this action]

        """
        links = [request.host_url + 'test/1']
        return success_response(
            tests=links
        )


class Test(Resource):  # test/id put get delete
    @jwt_required
    def delete(self, test_id):
        """
        ---
        summary: Change test by id
        description: Changes test
        requestBody:
          required: true
        content:
            application/json:
              schema: TestSchema
        responses:
            200:
                description: OK
            403:
                description: Not authorized
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Not allowed for this action]
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Test not found]

        """

        pass

    @jwt_required
    def put(self, test_id):
        """
        ---
        summary: Change test by id
        description: Changes test
        requestBody:
          required: true
        content:
            application/json:
              schema: TestSchema
        responses:
            200:
                description: OK
            403:
                description: Not authorized
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Not allowed for this action]
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Test not found]

        """
        pass

    @jwt_required
    def get(self, test_id):
        """
                ---
                summary: Get test by id
                description: All test questions with test metainfo
                parameters:
                    - in: path
                      name: user_id
                      schema:
                        type: integer
                      required: true
                      description: Numeric ID of the user to get
                responses:
                    200:
                        description: OK
                        content:
                            application/json:
                                schema: TestSchema
                    403:
                        description: Not authorized
                        content:
                            application/json:
                                schema: ErrorSchema
                                example:
                                  message: [Not allowed for this action]
                    404:
                        description: Not found
                        content:
                            application/json:
                                schema: ErrorSchema
                                example:
                                  message: [Test not found]

        """
        if not Utils.is_test_exist(test_id):
            return fail_response(msg="Test is not exist", code=404)




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
