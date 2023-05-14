from marshmallow import Schema, fields


#TODO: Better analyze this schema and improve it with more 
# required fields and create a new one for login only
class PlainUserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.Str()
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Int()


class PlainVehicleSchema(Schema):
    id = fields.String(dump_only=True)
    manufacturer = fields.Str(required=True)
    model = fields.Str(required=True)
    license_plate = fields.Str(required=True)
    consumption = fields.Float(required=True)


class UserSchema(PlainUserSchema):
    vehicles = fields.List(fields.Nested(PlainVehicleSchema()), dump_only=True, many=True)


class VehicleSchema(PlainVehicleSchema):
    user_id = fields.String(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
