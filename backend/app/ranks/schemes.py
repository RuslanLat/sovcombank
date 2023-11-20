from marshmallow import Schema, fields


class RankSchema(Schema):
    rank = fields.Str(required=True)


class RankRequestSchema(RankSchema):
    pass


class RankResponseSchema(Schema):
    id = fields.Int(required=True)
    rank = fields.Str(required=True)


class RankListResponseSchema(Schema):
    ranks = fields.Nested(RankResponseSchema, many=True)
