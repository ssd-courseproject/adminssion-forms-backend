from flask_jwt_extended import jwt_required
from flask_restful import Resource


class SubmissionsManagement(Resource):
    @jwt_required
    def get(self, submission_id):
        """
        ---
        summary: Submission info
        description: Candidate test submission information
        """
        pass


class SubmissionCheckpoint(Resource):
    @jwt_required
    def put(self, submission_id):
        """
        ---
        summary: Test checkpoint
        description: Saves current answers for test
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
        """
        pass
