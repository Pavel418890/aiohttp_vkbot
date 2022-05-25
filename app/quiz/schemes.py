from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class ThemeIdSchema(Schema):
    id = fields.Int(required=False)


class ThemeSchema(ThemeIdSchema):
    title = fields.Str(required=True)


class ThemeListSchema(Schema):
    themes = fields.Nested(ThemeSchema, many=True)


class ThemeResponseSchema(OkResponseSchema):
    data = fields.Nested(ThemeSchema)


class ThemeListResponseSchema(OkResponseSchema):
    data = fields.Nested(ThemeListSchema)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionIdSchema(Schema):
    id = fields.Int(requied=False)


class QuestionSchema(QuestionIdSchema):
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(AnswerSchema, many=True)


class QuestionListSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)


class QuestionResponseSchema(OkResponseSchema):
    data = fields.Nested(QuestionSchema)


class QuestionListResponseSchema(OkResponseSchema):
    data = fields.Nested(QuestionListSchema)
