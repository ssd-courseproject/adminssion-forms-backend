from flask_marshmallow import Schema
from marshmallow import fields


class ErrorSchema(Schema):
    message = fields.List(fields.Str())


class LoginSchema(Schema):
    class Meta:
        strict = True

    email = fields.Str(required=True, error_messages={'required': 'Email is required'})
    password = fields.Str(required=True, error_messages={'required': 'Password is required'})


class TokensSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
