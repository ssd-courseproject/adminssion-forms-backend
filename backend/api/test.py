from flask.json import jsonify
from flask_jwt_extended import jwt_required, get_current_user
from flask_restful import Resource
from marshmallow import fields
from webargs.flaskparser import use_kwargs, use_args

from backend.core import enums
from backend.core.decorators import candidate_role_required
from backend.core.models import Users
from backend.core.schema import TestsRegistrationSchema, TestsSchema, TestsSubmissionsSchema, QuestionsSchema
from backend.helpers import fail_response, generic_response, success_response
from server import application


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
                            example: [
                                {
                                    "archived": false,
                                    "id": 4,
                                    "max_time": null,
                                    "questions_tests": [],
                                    "test_name": "4"
                                }, {
                                    "archived": false,
                                    "id": 5,
                                    "max_time": null,
                                    "questions_tests": [],
                                    "test_name": "4"
                                }
                            ]
            406:
                description: Forbidden
                content:
                  application/json:
                    schema: ErrorSchema
                    example:
                      message: [You are not allowed to create test]
            404:
                description: Tests not found
                content:
                      application/json:
                        schema: ErrorSchema

        """
        user: Users = get_current_user()
        if user.user.role == enums.UsersRole.MANAGER or user.user.role == enums.UsersRole.STAFF:
            return fail_response(msg="You are not allowed to create test", code=406)
        tests = application.orm.get_tests()
        if tests is None:
            return fail_response("Some problems with tests retrieving", code=404)
        test_schema = TestsSchema(many=True)
        res = test_schema.dump(tests)

        return jsonify(res.data)


class TestCreation(Resource):
    @jwt_required
    @use_args(TestsRegistrationSchema, locations=("json",))
    def post(self, args):
        """
        ---
        summary: Test creation
        description: Creates new test
        requestBody:
          required: true
          content:
            application/json:
              schema: TestsRegistrationSchema
        responses:
          201:
            description: OK
          400:
                description: Bad request
                content:
                  application/json:
                    schema: ErrorSchema
                    example:
                      message: [Wrong input data]
        """
        test_name = args['test'].test_name
        test_time = args['test'].max_time
        if test_name is None or test_time is None:
            return fail_response(msg="Wrong input data", code=400)
        test_id = application.orm.add_test(test_name=test_name, max_time=test_time)
        for question in args['questions']:
            application.orm.add_question(question=question.question, question_type=question.question_type,
                                         answer=question.answer, manually_grading=question.manually_grading,
                                         points=question.points, test_id=int(test_id))
        if test_id is None:
            return fail_response("Test creation failed", code=500)
        return generic_response(status='Created', msg="Test created", code=201)


class TestManagement(Resource):
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
                        example: {
                                    "archived": false,
                                    "id": 8,
                                    "max_time": null,
                                    "questions": [
                                        {
                                            "answer": "1",
                                            "id": 5,
                                            "manually_grading": true,
                                            "points": 0,
                                            "question": "2",
                                            "question_type": 0,
                                            "test": 5
                                        },
                                        {
                                            "answer": "1",
                                            "id": 9,
                                            "manually_grading": true,
                                            "points": 0,
                                            "question": "2",
                                            "question_type": 0,
                                            "test": 9
                                        }
                                    ],
                                    "questions_tests": [
                                        5,
                                        9
                                    ],
                                    "test_name": "45"
                                }
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Test not found]
        """
        test = application.orm.get_test(test_id)
        test_schema = TestsSchema()
        if test is None:
            return fail_response("Test is not found", code=404)
        res = test_schema.dump(test)
        questions = []
        questions_schema = QuestionsSchema()
        for question_id in res.data['questions_tests']:
            obj = application.orm.get_question(question_id)
            questions.append(questions_schema.dump(obj).data)
        res.data.update({'questions': questions})
        return jsonify(res.data)

    @jwt_required
    @use_kwargs({"test_id": fields.Int(location="query")})
    @use_args(TestsRegistrationSchema())
    def put(self, args, test_id):
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
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Test not found]
            400:
                description: Bad request
                content:
                  application/json:
                    schema: ErrorSchema
                    example:
                      message: [Wrong input data]

        """
        test_name = args['test'].test_name
        test_time = args['test'].max_time
        req_test_id = args['test'].id
        if test_name is None or test_time is None or req_test_id is None:
            return fail_response(msg="Wrong input data", code=400)
        test_id = application.orm.update_test(test_id=args['test'].id, test_name=args['test'].test_name,
                                              max_time=args['test'].max_time)
        if test_id is None:
            return fail_response("Test is not found", code=404)
        for question in args['questions']:
            if question.id is None:
                application.orm.add_question(question=question.question, question_type=question.question_type,
                                             answer=question.answer, manually_grading=question.manually_grading,
                                             points=question.points, test_id=int(test_id))
            else:
                application.orm.update_question(question=question.question, question_type=question.question_type,
                                                answer=question.answer, manually_grading=question.manually_grading,
                                                points=question.points, test_id=int(test_id), question_id=question.id)
        return generic_response(status='Success', msg="Test changed", code=201)

    @jwt_required
    def delete(self, test_id):
        """
        ---
        summary: Delete test by id
        description: Deletes test
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
        success = application.orm.delete_test(test_id)
        if success:
            return generic_response(status='success', code=201, msg="Deleted")
        return fail_response(msg="Can't delete test", code=406)


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
                            items: TestsSubmissionsSchema
            404:
                description: Not found
                content:
                    application/json:
                        schema: ErrorSchema
                        example:
                          message: [Submission not found]
        """
        submissions = application.orm.get_submissions(test_id)
        if submissions is None:
            return fail_response("Submission not found", code=404)

        return TestsSubmissionsSchema(many=True).dump(submissions)


class TestStart(Resource):
    @jwt_required
    @candidate_role_required
    # @use_kwargs({"test_id": fields.Int(location="query")})
    def post(self, test_id):
        """
        ---
        summary: Test start
        description: Starts picked test for user and creates empty submission checkpoint
        parameters:
            - in: path
              required: true
              name: test_id
              schema:
                  type: int
        responses:
            201:
                description: OK
        """
        user: Users = get_current_user()

        submission = application.orm.init_submission(candidate_id=user.id, test_id=test_id)
        if submission is None:
            return fail_response("Submission was not created", code=406)

        return success_response(msg=submission.id, code=201)
