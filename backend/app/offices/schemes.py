from marshmallow import Schema, fields


class OfficeSchema(Schema):
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    lat = fields.Float()
    lon = fields.Float()
    


class OfficeRequestSchema(OfficeSchema):
    pass


class OfficeIdResponseSchema(Schema):
    id = fields.Int(required=True)
    addresse_id = fields.Int(required=True)


class OfficeResponseSchema(Schema):
    id = fields.Int(required=True)
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    lat = fields.Float()
    lon = fields.Float()
    


class OfficeListResponseSchema(Schema):
    offices = fields.Nested(OfficeResponseSchema, many=True)


class OfficeIdListResponseSchema(Schema):
    offices = fields.Nested(OfficeIdResponseSchema, many=True)
