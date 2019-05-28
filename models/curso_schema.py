from marshmallow import Schema, fields


class CursoSchema(Schema):
    id = fields.Str()
    nome = fields.Str(required=True, allow_none=False, strict=True)
    carga_horaria = fields.Integer(required=True, allow_none=False)
