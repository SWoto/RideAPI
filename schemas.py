from marshmallow import Schema, fields

class UserSchema(Schema):
    id=fields.String(dump_only=True)
    username = fields.Str()
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Int()