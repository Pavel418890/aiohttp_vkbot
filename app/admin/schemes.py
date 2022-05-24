from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class AdminRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AdminResponseSchema(OkResponseSchema):
    id = fields.Integer()
    email = fields.Str()

