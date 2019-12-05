from marshmallow import Schema, fields, validate


class RequestParseSchema(Schema):
    url = fields.Str(
        validate=validate.Length(min=4, max=255), required=True, nullable=False, load_only=True
    )
    cls = fields.Str(
        validate=validate.Length(max=150), required=True, nullable=False, load_only=True
    )
    elem = fields.Str(
        validate=validate.Length(max=30), required=True, nullable=False, load_only=True
    )
