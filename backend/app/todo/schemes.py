from marshmallow import Schema, fields


class ToDoSchema(Schema):
    user_id = fields.Int(required=True)
    office_id = fields.Int(required=True)
    partner_id = fields.Int(required=True)
    problem_id = fields.Int(required=True)
    queue = fields.Int(required=True)
    duration = fields.Float()
    length = fields.Float()

class ToDoRequestSchema(ToDoSchema):
    pass


class ToDoIdResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    office_id = fields.Int(required=True)
    partner_id = fields.Int(required=True)
    problem_id = fields.Int(required=True)
    queue = fields.Int(required=True)
    status = fields.Bool()
    message = fields.Str()
    duration = fields.Float()
    length = fields.Float()


class ToDoResponseSchema(Schema):
    id = fields.Int(required=True)
    surname = fields.Str(required=True)
    name = fields.Str(required=True)
    patronymic = fields.Str(required=True)
    city = fields.Str(required=True)
    addresse = fields.Str(required=True)
    lon = fields.Float(required=True)
    lat = fields.Float(required=True)
    partner = fields.Str(required=True)
    partner_city = fields.Str(required=True)
    partner_addresse = fields.Str(required=True)
    partner_lon = fields.Float(required=True)
    partner_lat = fields.Float(required=True)
    problem = fields.Str(required=True)
    queue = fields.Int(required=True)
    status = fields.Bool(required=True)
    message = fields.Str()
    duration = fields.Float()
    length = fields.Float()


class ToDoUpdateRequestSchema(Schema):
    surname = fields.Str(required=True)
    name = fields.Str(required=True)
    patronymic = fields.Str(required=True)
    partner = fields.Str(required=True)
    message = fields.Str()


class ToDoListeRequestSchema(Schema):
    surname = fields.Str(required=True)
    name = fields.Str(required=True)
    patronymic = fields.Str(required=True)


class ToDoIdDeleteResponseSchema(Schema):
    id = fields.Int(required=True)


class ToDoIdListResponseSchema(Schema):
    todos = fields.Nested(ToDoIdResponseSchema, many=True)


class ToDoListResponseSchema(Schema):
    todos = fields.Nested(ToDoResponseSchema, many=True)
