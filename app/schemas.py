from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    published_date = fields.Str(required=True)
    isbn = fields.Str(required=True)
    quantity = fields.Int(required=True)
    available = fields.Int(required=True)
    

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)