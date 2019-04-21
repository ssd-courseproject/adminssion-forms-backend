from flask.json import jsonify
from flask_restful import Resource
from marshmallow import fields
from webargs.flaskparser import use_kwargs, use_args

from backend.core.schema import TestsRegistrationSchema, TestsSchema, TestsSubmissionsSchema, QuestionsSchema
from backend.helpers import fail_response, generic_response
from server import application


class TestsList(Resource):
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
        """
        tests = application.orm.get_tests()
        if tests is None:
            return fail_response("Some problems with tests retreiving")
        test_schema = TestsSchema(many=True)
        res = test_schema.dump(tests)
        return jsonify(res.data)


class TestCreation(Resource):
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
        """
        test_id = application.orm.add_test(test_name=args['test'].test_name, max_time=args['test'].max_time)
        for question in args['questions']:
            application.orm.add_question(question=question.question, question_type=question.question_type,
                                         answer=question.answer, manually_grading=question.manually_grading,
                                         points=question.points, test_id=int(test_id))
        return generic_response(status='Created', msg="Test created", code=201)


class TestManagement(Resource):
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

        """
        test_id = application.orm.update_test(test_id=args['test'].id, test_name=args['test'].test_name,
                                              max_time=args['test'].max_time)
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
        return fail_response(msg="Cant delete test")


class TestSubmissions(Resource):
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
                          message: [Test not found]
        """
        submissions = application.orm.get_submissions(test_id)
        if submissions is None:
            return fail_response("Some problems with submissions retreiving")
        test_schema = TestsSubmissionsSchema(many=True)
        res = test_schema.dump(submissions)
        return jsonify(res.data)


class TestStart(Resource):
    @use_kwargs({"test_id": fields.Int(location="query")})
    @use_args({"test_id": fields.Int(), "candidate_id": fields.Int()}, locations=("json",))
    def post(self, args, test_id):
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
        requestBody:
          required: true
          content:
            application/json:
              schema: TestsSubmissionsSchema
        responses:
            201:
                description: OK
        """

        submission_id = application.orm.init_submission(candidate_id=args['candidate_id'], test_id=args['test_id'])
        return generic_response(status='Created', msg=submission_id, code=201)
