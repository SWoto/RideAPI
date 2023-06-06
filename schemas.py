from marshmallow import Schema, fields, validates_schema, ValidationError, validates
import re


class PlainUserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class PlainVehicleSchema(Schema):
    id = fields.String(dump_only=True)
    manufacturer = fields.Str(required=True)
    model = fields.Str(required=True)
    license_plate = fields.Str(required=True)
    consumption = fields.Float(required=True)
    active       = fields.Boolean(dump_only=True)

    @validates(field_name="license_plate")
    def validate_license_plate(self, data):
        match = re.search(r'[A-Z]{3}[0-9][0-9A-Z][0-9]{2}', data)
        if not match:
            raise ValidationError(
                "Invalid license plate format. Expected format is the vehicle registration plates of the Mercosur")

    @validates(field_name="consumption")
    def validate_consumption(self, data):
        if data <= 0 or data >= 100:
            raise ValidationError(
                "Invalid consumption. Accepted range 0 < x < 100")


class PlainRideSchema(Schema):
    id = fields.String(dump_only=True)
    distance = fields.Float(required=True)
    gas_price = fields.Float(required=True)
    total_value = fields.Float(dump_only=True)


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


class RideSchema(PlainRideSchema):
    user_id = fields.String(required=True, load_only=True)
    driver_id = fields.String(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    driver = fields.Nested(PlainUserSchema(), dump_only=True)
