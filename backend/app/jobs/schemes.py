from marshmallow import Schema, fields


class UserJobRequestSchema(Schema):
    surname = fields.Str(required=True)
    name = fields.Str(required=True)
    patronymic = fields.Str(required=True)
    position = fields.Str(required=True)
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    lon = fields.Float()
    lat = fields.Float()
    rank = fields.Str(required=True)


class UserJobIdResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    addresse_id = fields.Int(required=True)
    position_id = fields.Int(required=True)
    rank_id = fields.Int(required=True)


class UserJobResponseSchema(Schema):
    id = fields.Int(required=True)
    surname = fields.Str(required=True)
    name = fields.Str(required=True)
    patronymic = fields.Str(required=True)
    position = fields.Str(required=True)
    rank = fields.Str(required=True)
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    lon = fields.Float()
    lat = fields.Float()


class UserJobIdDeleteResponseSchema(Schema):
    id = fields.Int(required=True)


class UserJobDeleteResponseSchema(Schema):
    surname = fields.Str(required=True)
    name = fields.Str(required=True)
    patronymic = fields.Str(required=True)


class UserJobIdListResponseSchema(Schema):
    user_jobs = fields.Nested(UserJobIdResponseSchema, many=True)


class UserJobListResponseSchema(Schema):
    user_jobs = fields.Nested(UserJobResponseSchema, many=True)
