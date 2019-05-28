from marshmallow import Schema, fields


class CursoSchema(Schema):
    id = fields.Str(80)
    nome = fields.Str(80)
    carga_horaria = fields.Str(100)
