from marshmallow import Schema, fields


class MatriculaSchema(Schema):
    id = fields.Str()
    id_aluno = fields.Str(required=True, allow_none=False)
    id_curso = fields.Str(required=True, allow_none=False)
    data = fields.Str()
