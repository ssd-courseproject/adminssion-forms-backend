from flask_jwt_extended import jwt_required
from flask_restful import Resource


class SubmissionsManagement(Resource):
    @jwt_required
    def get(self, submission_id):
        """
        ---
        summary: Submission info
        description: Candidate test submission information
        parameters:
            - in: path
              required: true
              name: submission_id
              schema:
                  type: int
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: array
                            items: TestsSubmissions
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Test not found]
        """
        pass


class SubmissionCheckpoint(Resource):
    @jwt_required
    def put(self, submission_id):
        """
        ---
        summary: Test checkpoint
        description: Saves current answers for test
        parameters:
            - in: path
              required: true
              name: submission_id
              schema:
                  type: int
        requestBody:
            required: true
            content:
                application/json:
                  schema: TestsSubmissions
        responses:
            201:
                description: OK
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Test not found]

        """
        pass


class SubmissionComplete(Resource):
    @jwt_required
    def post(self, submission_id):
        """
        ---
        summary: Test submission
        description:
            Marks test as completed. After this action no checkpoints are allowed,
            so you have to firstly save answers and then complete test
        parameters:
            - in: path
              required: true
              name: submission_id
              schema:
                  type: int
        requestBody:
            required: true
            content:
                application/json:
                  schema: TestsSubmissions
        responses:
            201:
                description: OK
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Test not found]

        """
        pass
