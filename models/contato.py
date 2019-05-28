

class Contato():
    def __init__(self, id, nome, canal, valor, obs):
        self.id = id
        self.nome = nome
        self.canal = canal
        self.valor = valor
        self.obs = obs

    def __str__(self):
        return '{} {} {} {} {}'.format(self.id, self.nome, self.canal, self.valor, self.obs)

    def __repr__(self):
        return '<Contato(nome={self.nome})>'.format(self=self)
