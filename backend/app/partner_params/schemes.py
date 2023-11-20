from marshmallow import Schema, fields


class PartnerParamSchema(Schema):
    partner = fields.Str(required=True)
    delivered = fields.Bool(required=True)
    num_days = fields.Int(required=True)
    num_applications = fields.Int(required=True)
    num_cards = fields.Int(required=True)


class PartnerParamRequestSchema(PartnerParamSchema):
    pass


class PartnerParamDeleteResponseSchema(Schema):
    created_at = fields.DateTime(required=True)
    partner = fields.Str(required=True)


class PartnerParamIdResponseSchema(Schema):
    id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    partner_id = fields.Int(required=True)
    delivered = fields.Bool(required=True)
    num_days = fields.Int(required=True)
    num_applications = fields.Int(required=True)
    num_cards = fields.Int(required=True)


class PartnerParamResponseSchema(Schema):
    id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    partner = fields.Str(required=True)
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    data_connect = fields.Str(required=True)
    delivered = fields.Bool(required=True)
    num_days = fields.Int(required=True)
    num_applications = fields.Int(required=True)
    num_cards = fields.Int(required=True)


class PartnerParamIdDeleteResponseSchema(Schema):
    id = fields.Int(required=True)


class PartnerParamIdListResponseSchema(Schema):
    partner_params = fields.Nested(PartnerParamIdResponseSchema, many=True)


class PartnerParamListResponseSchema(Schema):
    partner_params = fields.Nested(PartnerParamResponseSchema, many=True)
