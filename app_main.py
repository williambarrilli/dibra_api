from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_swagger import swagger
from models.aluno_schema import AlunoSchema
from models.curso_schema import CursoSchema
from models.matricula_schema import MatriculaSchema
from uuid import uuid4
from datetime import datetime
from enum import Enum
# from dao.db import db

app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)
#  = "/api/components/schemas"


class Messages():
    EMPTY = "Dados vazios"
    NONE = "Resultado não encontrado!"
    CREATED = "Criado com sucesso!"
    UPDATED = "Atualizado com sucesso!"
    DELETED = "Removido com sucesso!"


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Dibra API"
    return jsonify(swag)


def gera_id():
    return str(uuid4())


@app.route("/")
def home():
    return " Driba API "


@app.route("/aluno", methods=['GET'])
def get_all_alunos():
    matriculas = mongo.db.matriculas
    alunos = mongo.db.alunos
    retorno = []

    for aluno_obj in alunos.find():
        id_alunos = []
        for matricula in matriculas.find():
            if aluno_obj['id'] == matricula['id_aluno']:
                id_alunos.append(matricula['id_aluno'])
        id_alunos_not_equals = set(id_alunos)

        soma_cursos = 0

        for quantidade in id_alunos_not_equals:
            soma_cursos = id_alunos.count(quantidade)

        retorno.append(
            {'id': aluno_obj['id'],
             'nome': aluno_obj['nome'],
             'sobrenome': aluno_obj['sobrenome'],
             'data_nascimento': aluno_obj['data_nascimento'],
             'cpf': aluno_obj['cpf'],
             'cursos_matriculados': soma_cursos})
        if len(retorno) == 0:
            return jsonify({"data": Messages.NONE})

    return jsonify({'alunos': retorno})


@app.route("/aluno/<aluno_id>", methods=['GET'])
def get_aluno(aluno_id=None):
    matriculas = mongo.db.matriculas
    alunos = mongo.db.alunos
    aluno_obj = alunos.find_one({'id': aluno_id})

    if not aluno_obj:
        return jsonify(Messages.NONE)

    id_alunos = []
    for matricula in matriculas.find():
        if aluno_id == matricula['id_aluno']:
            id_alunos.append(matricula['id_aluno'])
    id_alunos_not_equals = set(id_alunos)

    soma_cursos = 0

    for quantidade in id_alunos_not_equals:
        soma_cursos = id_alunos.count(quantidade)

    aluno_obj.pop('_id')
    aluno_obj.update({'cursos_matriculados': soma_cursos})
    return jsonify(aluno_obj)


@app.route("/aluno", methods=['POST'])
def create_aluno():
    alunos = mongo.db.alunos
    request_obj = AlunoSchema().load(request.get_json())

    print(request_obj.data)
    if request_obj.errors:
        return jsonify({"errorCode": [request_obj.errors]}), 404

    request_data = request_obj.data
    nome = request_data['nome']
    sobrenome = request_data['sobrenome']
    data_nascimento = request_data['data_nascimento']
    cpf = request_data['cpf']

    aluno_id = gera_id()

    alunos.insert_one({
        'id': aluno_id,
        'nome': nome,
        'sobrenome': sobrenome,
        'data_nascimento': data_nascimento,
        'cpf': cpf})

    return jsonify({'data': Messages.CREATED, "id": aluno_id}), 200


@app.route("/aluno/<aluno_id>", methods=['PUT'])
def set_aluno_name(aluno_id):
    request_data = request.get_json()
    nome = request_data['nome']
    sobrenome = request_data['sobrenome']
    data_nascimento = request_data['data_nascimento']
    cpf = request_data['cpf']

    mongo.db.alunos.update_one(
        {"id": aluno_id},
        {
            "$set": {
                "nome": nome,
                "sobrenome": sobrenome,
                "data_nascimento": data_nascimento,
                "cpf": cpf
            }
        }
    )

    return jsonify({"data": Messages.UPDATED})


@app.route("/aluno/<aluno_id>", methods=['DELETE'])
def delete_aluno(aluno_id):
    mongo.db.alunos.remove({'id': aluno_id})

    alunos = mongo.db.alunos
    aluno_obj = alunos.find_one({'id': aluno_id})
    if aluno_obj is not None:
        retorno = Messages.EMPTY
    else:
        retorno = Messages.DELETED
    return jsonify({'data': retorno})


@app.route("/aluno/totais/<aluno_id>", methods=['GET'])
def get_totais_alunos(aluno_id):
    matriculas = mongo.db.matriculas
    alunos = mongo.db.alunos

    id_alunos = []
    for matricula in matriculas.find():
        if aluno_id == matricula['id_aluno']:
            id_alunos.append(matricula['id_aluno'])
    id_alunos_not_equals = set(id_alunos)

    soma_alunos = 0

    for quantidade in id_alunos_not_equals:
        soma_alunos = id_alunos.count(quantidade)

    return jsonify({'Total de cursos matriculados': soma_alunos})


@app.route("/curso", methods=['GET'])
def get_all_cursos():
    matriculas = mongo.db.matriculas
    cursos = mongo.db.cursos
    retorno = []
    for curso_obj in cursos.find():
        id_cursos = []
        for matricula in matriculas.find():
            if curso_obj['id'] == matricula['id_curso']:
                id_cursos.append(matricula['id_curso'])
        id_cursos_not_equals = set(id_cursos)

        soma_cursos = 0

        for quantidade in id_cursos_not_equals:
            soma_cursos = id_cursos.count(quantidade)

        retorno.append(
            {'id': curso_obj['id'],
             'nome': curso_obj['nome'],
             'carga_horaria': curso_obj['carga_horaria'],
             'quantidade de inscritos': soma_cursos})

        if len(retorno) == 0:
            return jsonify({"message": Messages.EMPTY})

    return jsonify({'data': retorno})


@app.route("/curso/<curso_id>", methods=['GET'])
def get_curso(curso_id=None):
    matriculas = mongo.db.matriculas
    cursos = mongo.db.cursos
    curso_obj = cursos.find_one({'id': curso_id})

    if not curso_obj:
        return jsonify({"message": "Curso não encontrado!"})

    id_cursos = []

    for matricula in matriculas.find():
        if curso_obj['id'] == matricula['id_curso']:
            id_cursos.append(matricula['id_curso'])
    id_cursos_not_equals = set(id_cursos)

    soma_cursos = 0

    for quantidade in id_cursos_not_equals:
        soma_cursos = id_cursos.count(quantidade)

    curso_obj.pop('_id')
    curso_obj.update({'quantidade de inscritos': soma_cursos})

    return jsonify(curso_obj)


@app.route("/curso", methods=['POST'])
def create_curso():
    request_obj = CursoSchema().load(request.get_json())
    if request_obj.errors:
        return jsonify({"errorCode": [request_obj.errors]})

    nome = request.json['nome']
    carga_horaria = request.json['carga_horaria']

    cursos = mongo.db.cursos
    cursos.insert({
        'id': gera_id(),
        'nome': nome,
        'carga_horaria': carga_horaria})

    return jsonify({'data': Messages.CREATED})


@app.route("/curso/<curso_id>", methods=['PUT'])
def update_curso(curso_id=None):
    request_obj = CursoSchema().load(request.get_json())
    if request_obj.errors:
        return jsonify({"errorCode": [request_obj.errors]})

    request_data = request_obj.data
    mongo.db.cursos.update_one(
        {"id": curso_id},
        {
            "$set": {
                "nome": request_data['nome'],
                "carga_horaria": request_data['carga_horaria']
            }
        }
    )

    return jsonify({"data": Messages.UPDATED}), 201


@app.route("/curso/<curso_id>", methods=['DELETE'])
def delete_curso(curso_id=None):
    mongo.db.cursos.remove({'id': curso_id})

    cursos = mongo.db.cursos
    curso_obj = cursos.find_one({'id': curso_id})
    if curso_obj is not None:
        retorno = "Erro ao excluir curso"
    else:
        retorno = Messages.DELETED
    return jsonify({'data': retorno})


@app.route("/curso/totais", methods=['GET'])
def get_totais():
    matriculas = mongo.db.matriculas
    cursos = mongo.db.cursos

    id_cursos = []
    for matricula in matriculas.find():
        id_cursos.append(matricula['id_curso'])

    id_cursos_not_equals = set(id_cursos)
    nome_cursos = []

    for curso in id_cursos_not_equals:
        cursos_obj = cursos.find_one({'id': curso})
        if cursos_obj:
            nome = cursos_obj['nome']
            nome_cursos.append(nome)

    soma_cursos = []

    for quantidade in id_cursos_not_equals:
        soma_cursos.append(id_cursos.count(quantidade))

    dict_cursos = dict(zip(nome_cursos, soma_cursos))

    return jsonify({'Totais de matriculados': dict_cursos})


@app.route("/matricula", methods=['POST'])
def create_matricula():
    alunos = mongo.db.alunos
    cursos = mongo.db.cursos
    matriculas = mongo.db.matriculas
    id_aluno = request.json['id_aluno']
    id_curso = request.json['id_curso']
    data = datetime.now()

    valid_id_aluno = alunos.find_one({'id': id_aluno})
    if not valid_id_aluno:
        retorno = "id do aluno não encontrado"
        return jsonify(retorno)

    valid_id_curso = cursos.find_one({'id': id_curso})
    if not valid_id_curso:
        retorno = "id do curso não encontrado"
        return jsonify(retorno)
    id = gera_id()
    matriculas.insert({
        'id': id,
        'id_aluno': id_aluno,
        'id_curso': id_curso,
        'data': data})

    return jsonify({'data': Messages.CREATED, "id": id})


@app.route("/matricula/<matricula_id>", methods=['DELETE'])
def delete_matricula(matricula_id):
    mongo.db.matriculas.remove({'id': matricula_id})

    matriculas = mongo.db.matriculas
    matricula_obj = matriculas.find_one({'id': matricula_id})
    if matricula_obj is not None:
        retorno = "Error"
    else:
        retorno = "matricula excluido"
    return jsonify({'mensagem': retorno})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
