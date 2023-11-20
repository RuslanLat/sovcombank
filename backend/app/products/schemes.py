from marshmallow import Schema, fields


class ProductSchema(Schema):
    product = fields.Str(required=True)
    description = fields.Str(required=True)


class ProductRequestSchema(ProductSchema):
    pass


class ProductDeleteRequestSchema(Schema):
    product = fields.Str(required=True)


class ProductResponseSchema(Schema):
    id = fields.Int(required=True)
    product = fields.Str(required=True)
    description = fields.Str(required=True)


class ProductListResponseSchema(Schema):
    products = fields.Nested(ProductResponseSchema, many=True)