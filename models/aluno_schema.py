from marshmallow import Schema, fields, ValidationError, validates


class AlunoSchema(Schema):
    id = fields.Str(80)
    nome = fields.Str(required=True, allow_none=False)
    sobrenome = fields.Str(required=True, allow_none=False)
    data_nascimento = fields.Str(required=True, allow_none=False)
    cpf = fields.Str(required=True, allow_none=False)

    @validates('cpf')
    def validate_cpf(self, data):
        cpf_invalidos = [11*str(i) for i in range(10)]
        cpf = data
        if cpf in cpf_invalidos:
            raise ValidationError('CPF inválido!')

        if not cpf.isdigit():
            """ Verifica se o CPF contem pontos e hifens e faz o replace """
            cpf = cpf.replace('.', "")
            cpf = cpf.replace('-', "")

        if len(cpf) < 11:
            raise ValidationError('O tamanho do CPF não pode ser \
                                   menor do que 11 digitos')

        if len(cpf) > 11:
            raise ValidationError('O tamanho do CPF não pode ser \
                                   maior do que 11 digitos')

