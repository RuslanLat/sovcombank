from marshmallow import Schema, fields


class AddresseSchema(Schema):
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    lon = fields.Float()
    lat = fields.Float()


class AddresseRequestSchema(AddresseSchema):
    pass


class AddresseResponseSchema(Schema):
    id = fields.Int(required=True)
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    lon = fields.Float()
    lat = fields.Float()


class AddresseListResponseSchema(Schema):
    addresses = fields.Nested(AddresseResponseSchema, many=True)