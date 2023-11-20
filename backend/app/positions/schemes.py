from marshmallow import Schema, fields


class PositionSchema(Schema):
    position = fields.Str(required=True)


class PositionRequestSchema(PositionSchema):
    pass


class PositionResponseSchema(Schema):
    id = fields.Int(required=True)
    position = fields.Str(required=True)


class PositionListResponseSchema(Schema):
    positions = fields.Nested(PositionResponseSchema, many=True)
