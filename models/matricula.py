
class Matricula():
    def __init__(self, id, id_aluno, id_curso, data):
        self.id = id
        self.id_aluno = id_aluno
        self.id_curso = id_curso
        self.data = data

    def __str__(self):
        return '{} {} {} {} {}'.format(self.id, self.id_aluno, self.id_curso)

    def __repr__(self):
        return '<Matricula(nome={self.id_aluno, self.id_curso})>'.format(self=self)