import pymongo
from flask import Flask
from flask import jsonify
from flask import request
from models.aluno import Aluno
from model.aluno_schema import AlunoSchema
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


@app.route(BASE_URL + "/alunoCreate", methods=['POST'])
def create_aluno():
    request_data = request.get_json()
    new_aluno = Aluno(str(len(alunos) + 1), request_data['nome'],
                      request_data['canal'], request_data['valor'],
                      request_data['obs'])
    alunos.append(new_aluno)
    return jsonify(messages["created"])


@app.route(BASE_URL + "/alunoUpdate/<aluno_id>", methods=['PUT'])
def update_aluno(aluno_id=None):
    request_data = request.get_json()
    for aluno in alunos:
        if aluno.id == aluno_id:
            aluno.nome = request_data['nome']
            aluno.canal = request_data['canal']
            aluno.valor = request_data['valor']
            aluno.obs = request_data['obs']
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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
