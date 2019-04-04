from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs.flaskparser import use_kwargs

from backend.core.schema import TestSummarySchema


class TestsList(Resource):
    @jwt_required
    def get(self):
        """
        ---
        summary: Get all non-archived tests list
        description: All tests with links on them
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: array
                            items: TestsSchema
            403:
                description: Not authorized
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Not allowed for this action]

        """
        pass


class TestManagement(Resource):
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
              schema: TestsSchema
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
                        schema: TestsSchema
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
    @use_kwargs(TestSummarySchema)
    def put(self, test_id):
        """
        ---
        summary: Change test by id
        description: Changes test
        parameters:
            - in: path
              required: true
              name: test_id
              schema:
                  type: int
        requestBody:
            required: true
            content:
                application/json:
                  schema: TestsSchema
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
    def delete(self, test_id):
        """
        ---
        summary: Delete test by id
        description: Deletes test
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
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Test not found]

        """
        pass


class TestSubmissions(Resource):
    @jwt_required
    def get(self, test_id):
        """
        ---
        summary: Test submissions
        description: List of all submissions for given test
        parameters:
            - in: path
              required: true
              name: test_id
              schema:
                  type: int

        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: array
                            items: TestsSchema
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


class TestStart(Resource):
    @jwt_required
    def post(self, test_id):
        """
        ---
        summary: Test start
        description: Starts picked test for user and creates empty submission checkpoint
        responses:
            200:
                description: OK
        """
        pass
