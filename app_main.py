import pymongo
from flask import Flask
from flask import jsonify
from flask import request
from models.aluno import Aluno
from models.aluno_schema import AlunoSchema
from models.curso import Curso
from models.curso_schema import CursoSchema
from models.matricula import Matricula
from models.matricula_schema import MatriculaSchema

from dao.db import db

app = Flask(__name__)


# BASE_URL = "/api/components/schemas"
BASE_URL = "/api"

aluno_1 = Aluno('1', 'teste', 'email', 'teste1@teste.com', 'Email teste1')
aluno_2 = Aluno('2', 'teste2', 'email', 'teste2@teste.com', 'Email teste2')
aluno_3 = Aluno('3', 'teste3', 'email', 'teste3@teste.com', 'Email teste3')
aluno_4 = Aluno('4', 'teste4', 'email', 'teste4@teste.com', 'Email teste4')


alunos = [aluno_1, aluno_2, aluno_3, aluno_4]
messages = {
    "empty": {"message": "Dados vazios"},
    "none": {"message": "aluno nao encontrado!"},
    "created": {"message": "aluno criado com sucesso!"},
    "updated": {"message": "aluno atualizado com sucesso!"},
    "deleted": {"message": "aluno removido com sucesso!"}
}


@app.route(BASE_URL)
def index():
    return "API Dibra!"


@app.route(BASE_URL + "/aluno", methods=['GET'])
def get_alunos():
    print(len(alunos))
    if len(alunos) > 0:
        return jsonify(AlunoSchema(many=True).dump(alunos))
    return jsonify(messages["empty"])


@app.route(BASE_URL + "/aluno/<aluno_id>", methods=['GET'])
def get_aluno(aluno_id=None):
    print(aluno_id)
    for aluno in alunos:
        if aluno.id == aluno_id:
            return jsonify(AlunoSchema().dump(aluno))

    return jsonify(messages["empty"])


@app.route(BASE_URL + "/aluno", methods=['POST'])
def create_aluno():
    request_data = request.get_json()
    new_aluno = Aluno(str(len(alunos) + 1), request_data['nome'],
                      request_data['sobrenome'], request_data['cpf'],
                      request_data['data_nascimento'])
    alunos.append(new_aluno)
    return jsonify(messages["created"])


@app.route(BASE_URL + "/aluno/<aluno_id>", methods=['PUT'])
def update_aluno(aluno_id=None):
    request_data = request.get_json()
    for aluno in alunos:
        if aluno.id == aluno_id:
            aluno.nome = request_data['nome']
            aluno.sobrenome = request_data['sobrenome']
            aluno.cpf = request_data['cpf']
            aluno.data_nascimento = request_data['data_nascimento']
            return jsonify(messages["updated"])
    return jsonify(messages["empty"])


@app.route(BASE_URL + "/aluno/<aluno_id>", methods=['DELETE'])
def delete_aluno(aluno_id=None):
    for aluno in alunos:
        if aluno.id == aluno_id:
            print(alunos.index(aluno))
            alunos.pop()
            return jsonify(messages["deleted"])
        else:
            return jsonify(messages["none"])


# --------------CURSO


@app.route(BASE_URL + "/curso", methods=['GET'])
def get_cursos():
    print(len(curso))
    if len(curso) > 0:
        return jsonify(CursoSchema(many=True).dump(cursos))
    return jsonify(messages["empty"])


@app.route(BASE_URL + "/curso/<curso_id>", methods=['GET'])
def get_curso(curso_id=None):
    print(curso_id)
    for curso in cursos:
        if curso.id == curso_id:
            return jsonify(CursoSchema().dump(curso))

    return jsonify(messages["empty"])


@app.route(BASE_URL + "/curso", methods=['POST'])
def create_curso():
    request_data = request.get_json()
    new_curso = curso(str(len(cursos) + 1), request_data['nome'],
                      request_data['carga_horaria'])
    cursos.append(new_curso)
    return jsonify(messages["created"])


@app.route(BASE_URL + "/curso/<curso_id>", methods=['PUT'])
def update_curso(curso_id=None):
    request_data = request.get_json()
    for curso in cursos:
        if curso.id == curso_id:
            curso.nome = request_data['nome']
            curso.carga_horaria = request_data['carga_horaria']
            return jsonify(messages["updated"])
    return jsonify(messages["empty"])


@app.route(BASE_URL + "/curso/<curso_id>", methods=['DELETE'])
def delete_curso(curso_id=None):
    for curso in cursos:
        if curso.id == curso_id:
            print(cursos.index(curso))
            cursos.pop()
            return jsonify(messages["deleted"])
        else:
            return jsonify(messages["none"])


# ---------------MATRICULA


@app.route(BASE_URL + "/matricula", methods=['POST'])
def create_mat():
    request_data = request.get_json()
    new_Matricula = Matricula(str(len(matriculas) + 1), request_data['id_aluno'],
                              request_data['id_curso'], request_data['data'])
    matriculas.append(new_matricula)
    return jsonify(messages["created"])


@app.route(BASE_URL + "/matricula/<matricula_id>", methods=['DELETE'])
def delete_matricula(matricula_id=None):
    for matricula in matriculas:
        if matricula.id == matricula_id:
            print(matriculas.index(matricula))
            matriculas.pop()
            return jsonify(messages["deleted"])
        else:
            return jsonify(messages["none"])


if __name__ == '__main__':
    app.run(port=5000, debug=True)
