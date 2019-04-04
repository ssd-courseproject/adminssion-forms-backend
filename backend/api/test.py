from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs.flaskparser import use_kwargs

from backend.core.schema import TestSummarySchema


class TestsList(Resource):
    @jwt_required
    def get(self):
        """
        ---
        summary: Tests list
        description: List of non-archived tests
        """
        pass


class TestManagement(Resource):
    @jwt_required
    def post(self):
        """
        ---
        summary: Test create
        description: Creates new test by given information
        """
        pass

    @jwt_required
    def get(self, test_id):
        """
        ---
        summary: Test info
        description: Returns all relevant content of test
        """
        pass

    @jwt_required
    @use_kwargs(TestSummarySchema)
    def put(self, test_id):
        """
        ---
        summary: Test update
        description: Saves new test information
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
              schema: TestSummarySchema
        """
        pass

    @jwt_required
    def delete(self, test_id):
        """
        ---
        summary: Test archive
        description: Marks test as archived
        """
        pass


class TestSubmissions(Resource):
    @jwt_required
    def get(self, test_id):
        """
        ---
        summary: Test submissions
        description: List of all submissions for given test
        """
        pass


class TestStart(Resource):
    @jwt_required
    def post(self, test_id):
        """
        ---
        summary: Test start
        description: Starts picked test for user and creates empty submission checkpoint
        """
        pass
