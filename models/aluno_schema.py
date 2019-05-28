from marshmallow import Schema, fields, ValidationError, validates


class AlunoSchema(Schema):
    id = fields.Str(80)
    nome = fields.Str(80)
    sobrenome = fields.Str(100)
    data_nascimento = fields.Str(250)
    cpf = fields.Str(255)

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

        selfcpf = [int(x) for x in cpf]

        cpf = selfcpf[:9]

        while len(cpf) < 11:
            r = sum([(len(cpf)+1-i)*v
                     for i, v in [(x, cpf[x]) for x in range(len(cpf))]]) % 11

        if r > 1:
            f = 11 - r
        else:
            f = 0
        cpf.append(f)

        return cpf
