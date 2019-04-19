from flask import jsonify
from flask_restful import Resource
from marshmallow import fields
from webargs.flaskparser import use_kwargs, use_args

from backend.core.schema import TestsSubmissionsSchema, TestsSubmissionWithAnswersSchema, CandidatesAnswersSchema
from backend.helpers import success_response, fail_response, generic_response
from server import application


# +
class SubmissionsManagement(Resource):
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
                            items: TestsSubmissionsSchema
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Test not found]
        """
        submission = application.orm.get_submission(submission_id)
        submission_schema = TestsSubmissionsSchema()
        if submission is None:
            return fail_response("Test is not found", code=404)
        res = submission_schema.dump(submission)
        answers = application.orm.get_answers(res.data['id'])
        json_answers = []
        answers_schema = CandidatesAnswersSchema()
        for answer in answers:
            json_answers.append(answers_schema.dump(answer).data)
        res.data.update({'answers': json_answers})
        return jsonify(res.data)


class SubmissionCheckpoint(Resource):
    @use_kwargs({"submissions_id": fields.Int(location="query")})
    @use_args(TestsSubmissionWithAnswersSchema(), locations=("json",))
    def put(self, args, submission_id):
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
                  schema: TestsSubmissionsSchema
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
        for answer in args['answers']:
            res = application.orm.add_answer(submission_id=submission_id, question_id=answer.question_id,
                                             answer=answer.answer)
            if res is None:
                application.orm.update_answer(submission_id=submission_id, question_id=answer.question_id,
                                              answer=answer.answer, grade=answer.grade, comments=answer.comments)
        return success_response(msg="Answers saved")


class SubmissionComplete(Resource):
    @use_kwargs({"submissions_id": fields.Int(location="query")})
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
                  schema: TestsSubmissionsSchema
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
        test_id = application.orm.finish_submission(submission_id=submission_id)
        return generic_response(status='Created', msg="Submission completed", code=201)
