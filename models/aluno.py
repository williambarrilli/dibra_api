

class Aluno():
    def __init__(self, id, nome, sobrenome, data_nascimento, cpf):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __str__(self):
        return '{} {} {} {} {}'.format(self.id, self.nome, self.sobrenome,
                                       self.data_nascimento, self.cpf)

    def __repr__(self):
        return '<Aluno(nome={self.nome})>'.format(self=self)
