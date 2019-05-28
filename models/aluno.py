

class Aluno():
    def __init__(self, id, nome, sobrenome, data_nascimento, obs):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_nascimento = data_nascimento
        self.obs = obs

    def __str__(self):
        return '{} {} {} {} {}'.format(self.id, self.nome, self.sobrenome,
                                       self.data_nascimento, self.obs)

    def __repr__(self):
        return '<Aluno(nome={self.nome})>'.format(self=self)
