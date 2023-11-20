from marshmallow import Schema, fields


class ProblemSchema(Schema):
    problem_type = fields.Int(required=True)
    problem = fields.Str(required=True)
    priority = fields.Str(required=True)
    lead_time = fields.Str(required=True)
    condition_one = fields.Str(required=True)
    condition_two = fields.Str(required=True)
    rank = fields.Str(required=True)


class ProblemRequestSchema(ProblemSchema):
    pass


class ProblemDeleteRequestSchema(Schema):
    problem = fields.Str(required=True)

class ProblemResponseSchema(Schema):
    id = fields.Int(required=True)
    problem_type = fields.Int(required=True)
    problem = fields.Str(required=True)
    priority = fields.Str(required=True)
    lead_time = fields.Str(required=True)
    condition_one = fields.Str(required=True)
    condition_two = fields.Str(required=True)
    rank = fields.Str(required=True)


class ProblemListResponseSchema(Schema):
    problems = fields.Nested(ProblemResponseSchema, many=True)