from marshmallow import Schema, fields, pprint


class AlunoSchema(Schema):
    id = fields.Str(80)
    nome = fields.Str(80)
    canal = fields.Str(100)
    valor = fields.Str(250)
    obs = fields.Str(255)
