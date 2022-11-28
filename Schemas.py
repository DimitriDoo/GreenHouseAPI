from marshmallow import Schema, fields, validate

class GreenHouseInfoSchemaPost(Schema):
    greenhouseId = fields.Int(required=True)
    temp = fields.Float(required=True)
    humidity = fields.Float(required=True)
    lumens = fields.Float(required=True)

