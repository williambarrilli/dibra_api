
class Curso():
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def __str__(self):
        return '{} {} {} {} {}'.format(self.id, self.nome)

    def __repr__(self):
        return '<Curso(nome={self.nome})>'.format(self=self)
