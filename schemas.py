from marshmallow import Schema, fields, validates_schema, ValidationError
import re


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

    @validates_schema
    def validate_license_plate(self, data, **kwargs):
        match = re.search(r'[A-Z]{3}[0-9][0-9A-Z][0-9]{2}', data['license_plate'])
        if not match:
            raise ValidationError("Invalid license plate format. Expected format is the vehicle registration plates of the Mercosur")

    @validates_schema
    def validate_consumption(self, data, **kwargs):
        consumption = data['consumption']
        if consumption <= 0 or consumption >= 100:
            raise ValidationError("Invalid consumption. Accepted range 0 < x < 100")

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
