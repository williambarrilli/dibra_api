from marshmallow import Schema, fields


class AlunoSchema(Schema):
    id = fields.Str(80)
    nome = fields.Str(80)
    sobrenome = fields.Str(100)
    data_nascimento = fields.Str(250)
    cpf = fields.Str(255)
