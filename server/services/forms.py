from marshmallow import Schema, fields, validate


class TeamResponseSchema(Schema):
    team_id = fields.Int(required=True)
    name = fields.Str(validate=validate.Length(min=2, max=80), required=True, nullable=False)
    created_on = fields.DateTime()
    site_name = fields.Str(validate=validate.Length(min=2, max=25), required=True, nullable=False)
    real_team_id = fields.Int()
    link_id = fields.Int(required=True, nullable=False)
    status = fields.Str(
        validate=validate.OneOf(["new", "moderated", "approved"]), nullable=False
    )
