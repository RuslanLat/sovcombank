from marshmallow import Schema, fields


class PartnerSchema(Schema):
    partner = fields.Str(required=True)
    data_connect = fields.Str(required=True)
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    lat = fields.Float()
    lon = fields.Float()
    


class PartnerRequestSchema(PartnerSchema):
    pass


class PartnerIdResponseSchema(Schema):
    id = fields.Int(required=True)
    partner = fields.Str(required=True)
    data_connect = fields.Str(required=True)
    addresse_id = fields.Int(required=True)


class PartnerResponseSchema(Schema):
    id = fields.Int(required=True)
    partner = fields.Str(required=True)
    data_connect = fields.Str(required=True)
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    lat = fields.Float()
    lon = fields.Float()
    


class PartnerIdDeleteResponseSchema(Schema):
    id = fields.Int(required=True)


class PartnerDeleteRequestSchema(Schema):
    partner = fields.Str(required=True)


class PartnerIdListResponseSchema(Schema):
    partners = fields.Nested(PartnerIdResponseSchema, many=True)


class PartnerListResponseSchema(Schema):
    partners = fields.Nested(PartnerResponseSchema, many=True)