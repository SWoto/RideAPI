from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class PlainVehicleSchema(Schema):
    id = fields.String(dump_only=True)
    manufacturer = fields.Str(required=True)
    model = fields.Str(required=True)
    license_plate = fields.Str(required=True)
    consumption = fields.Float(required=True)


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRoleSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.Str(require=True)


class UserSchema(PlainUserSchema):
    role_id = fields.String(required=True, load_only=True)
    vehicles = fields.List(fields.Nested(
        PlainVehicleSchema()), dump_only=True, many=True)
    role = fields.Nested(UserRoleSchema(), dump_only=True)


class VehicleSchema(PlainVehicleSchema):
    user_id = fields.String(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
