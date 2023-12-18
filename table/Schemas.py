from marshmallow import Schema,fields

class User_schema(Schema):
    id = fields.Int(dump_only=True)
    name=fields.Str()
    email=fields.Str()
    password = fields.Str(load_only=True)


class Task_schema(Schema):
    id = fields.Int()
    task_name = fields.Str()
    date_created=fields.Str()

class Status_schema(Schema):
    id = fields.Int()
    status = fields.Str(required=True)

