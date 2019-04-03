from flask_marshmallow import Schema
from marshmallow import fields


class ErrorSchema(Schema):
    message = fields.Str()


class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class TokensSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
