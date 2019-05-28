from marshmallow import Schema, fields


class MatriculaSchema(Schema):
    id = fields.Str(80)
    id_aluno = fields.Str(80)
    id_curso = fields.Str(100)
    data = fields.Str(250)
