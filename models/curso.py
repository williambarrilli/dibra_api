
class Curso():
    def __init__(self, id, nome, carga_horaria):
        self.id = id
        self.nome = nome
        self.carga_horaria = carga_horaria

    def __str__(self):
        return '{} {} {} {} {}'.format(self.id, self.nome, self.carga_horaria)

    def __repr__(self):
        return '<Curso(nome={self.nome, self.carga_horaria})>'.format(self=self)
