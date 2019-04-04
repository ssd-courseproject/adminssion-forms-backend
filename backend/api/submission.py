from flask_restful import Resource


class SubmissionsList(Resource):
    def post(self, test_id):
        pass


class SubmissionsManagement(Resource):
    def get(self, submission_id):
        pass


class SubmissionCheckpoint(Resource):
    def put(self, submission_id):
        pass


class SubmissionComplete(Resource):
    def post(self, submission_id):
        pass
