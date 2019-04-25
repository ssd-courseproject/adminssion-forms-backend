from flask_marshmallow import Schema
from flask_marshmallow.sqla import ModelSchema
from marshmallow import fields
from marshmallow.validate import OneOf
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import field_for

from backend.core.enums import Gender
from backend.core.models import Users, UsersAutorization, CandidatesInfo, CandidatesInterview, CandidatesDocuments, \
    CandidatesStatus, CandidatesAnswers, TestsSubmissions, QuestionsTests, Tests, Questions


######
# Models based schemas
######

class UsersSchema(ModelSchema):
    class Meta:
        model = Users


class UsersAutorizationSchema(ModelSchema):
    class Meta:
        model = UsersAutorization

    password = field_for(UsersAutorization, "password", load_only=True)


class CandidatesInfoSchema(ModelSchema):
    class Meta:
        model = CandidatesInfo

    gender = EnumField(Gender, validate=OneOf(Gender.names()))


class CandidatesDocumentsSchema(ModelSchema):
    class Meta:
        model = CandidatesDocuments


class CandidatesStatusSchema(ModelSchema):
    class Meta:
        model = CandidatesStatus


class CandidatesInterviewSchema(ModelSchema):
    class Meta:
        model = CandidatesInterview


class CandidatesAnswersSchema(ModelSchema):
    class Meta:
        model = CandidatesAnswers

    question_id = field_for(CandidatesAnswers, 'question_id', dump_only=False)
    submission_id = field_for(CandidatesAnswers, 'submission_id', dump_only=False)


class TestsSubmissionsSchema(ModelSchema):
    class Meta:
        model = TestsSubmissions
        strict = True


class QuestionsTestsSchema(ModelSchema):
    class Meta:
        model = QuestionsTests


class TestsSchema(ModelSchema):
    class Meta:
        model = Tests


class QuestionsSchema(ModelSchema):
    class Meta:
        model = Questions


class TestsRegistrationSchema(Schema):
    test = fields.Nested(TestsSchema)
    questions = fields.List(fields.Nested(QuestionsSchema))


class TestsSubmissionWithAnswersSchema(Schema):
    submission = fields.Nested(TestsSubmissionsSchema)
    answers = fields.List(fields.Nested(CandidatesAnswersSchema))


######
# Core schemas
######

class ErrorSchema(Schema):
    message = fields.List(fields.Str())


######
# Common schemas
######

class LoginSchema(Schema):
    class Meta:
        strict = True

    email = fields.Str(required=True, error_messages={'required': 'Email is required'})
    password = fields.Str(required=True, error_messages={'required': 'Password is required'})


class RegistrationSchema(Schema):
    class Meta:
        strict = True

    email = fields.Str(required=True, error_messages={'required': 'Email is required'})
    password = fields.Str(required=True, error_messages={'required': 'Password is required'})
    name = fields.Str(required=True, error_messages={'required': 'Name is required'})
    surname = fields.Str(required=True, error_messages={'required': 'Surname is required'})


class TokensSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()


class HostSchema(Schema):
    host = fields.Str()
    host_full = fields.Str()


######
# Complex schemas
######

class ProfileInfoSchema(Schema):
    user = fields.Nested(UsersSchema, only=["first_name", "last_name", "role"])
    authentication = fields.Nested(UsersAutorizationSchema, exclude=["user"])
    info = fields.Nested(CandidatesInfoSchema, exclude=["user"])
    documents = fields.Nested(CandidatesDocumentsSchema, exclude=["user"])
    status = fields.Nested(CandidatesStatusSchema, exclude=["user"])


class TestSummarySchema(Schema):
    test = fields.Nested(TestsSchema)
