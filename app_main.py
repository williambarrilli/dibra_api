from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_swagger import swagger


# from models.aluno import Aluno
# from models.aluno_schema import AlunoSchema
# from models.curso import Curso
# from models.curso_schema import CursoSchema
# from models.matricula import Matricula
# from models.matricula_schema import MatriculaSchema
from uuid import uuid4
from datetime import datetime
# from dao.db import db

app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)
#  = "/api/components/schemas"

messages = {
    "empty": {"message": "Dados vazios"},
    "none": {"message": "aluno nao encontrado!"},
    "created": {"message": "aluno criado com sucesso!"},
    "updated": {"message": "aluno atualizado com sucesso!"},
    "deleted": {"message": "aluno removido com sucesso!"}
}


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
    alunos = mongo.db.alunos
    retorno = []
    for aluno_obj in alunos.find():
        retorno.append(
            {'id': aluno_obj['id'],
             'nome': aluno_obj['nome'],
             'sobrenome': aluno_obj['sobrenome'],
             'data_nascimento': aluno_obj['data_nascimento'],
             'cpf': aluno_obj['cpf']})
        if len(retorno) == 0:
            return jsonify({"message": "Não há alunos cadastrados!"})

    return jsonify({'alunos': retorno})


@app.route("/aluno/<aluno_id>", methods=['GET'])
def get_aluno(aluno_id=None):
    alunos = mongo.db.alunos
    aluno_obj = alunos.find_one({'id': aluno_id})
    if not aluno_obj:
        retorno = "aluno não encontrado"
        return jsonify(retorno)
    aluno_obj.pop('_id')
    return jsonify(aluno_obj)


@app.route("/aluno", methods=['POST'])
def create_aluno():
    alunos = mongo.db.alunos
    nome = request.json['nome']
    sobrenome = request.json['sobrenome']
    data_nascimento = request.json['data_nascimento']
    cpf = request.json['cpf']

    alunos.insert({
        'id': gera_id(),
        'nome': nome,
        'sobrenome': sobrenome,
        'data_nascimento': data_nascimento,
        'cpf': cpf})

    return jsonify({'result': 'ok', "id": id})


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

    return jsonify({"message": "Só por Deus"})


@app.route("/aluno/<aluno_id>", methods=['DELETE'])
def delete_aluno(aluno_id):
    mongo.db.alunos.remove({'id': aluno_id})

    alunos = mongo.db.alunos
    aluno_obj = alunos.find_one({'id': aluno_id})
    if aluno_obj != None:
        retorno = "Error"
    else:
        retorno = "aluno excluido"
    return jsonify({'mensagem': retorno})


@app.route("/curso", methods=['GET'])
def get_all_cursos():
    cursos = mongo.db.cursos
    retorno = []
    for cursos_obj in cursos.find():
        retorno.append(
            {'id': cursos_obj['id'],
             'nome': cursos_obj['nome'],
             'carga_horaria': cursos_obj['carga_horaria']})
        if len(retorno) == 0:
            return jsonify({"message": "Não há cursos cadastrados!"})

    return jsonify({'cursos': retorno})

@app.route("/curso/<curso_id>", methods=['GET'])
def get_curso(curso_id=None):
    cursos = mongo.db.cursos
    cursos_obj = cursos.find_one({'id': curso_id})
    if not cursos_obj:
        return jsonify({"message": "Curso não encontrado!"})

    cursos_obj.pop('_id')
    return jsonify(cursos_obj)


@app.route("/curso", methods=['POST'])
def create_curso():
    alunos = mongo.db.cursos
    nome = request.json['nome']
    carga_horaria = request.json['carga_horaria']

    alunos.insert({
        'id': gera_id(),
        'nome': nome,
        'carga_horaria': carga_horaria})

    return jsonify({'result': 'Curso criado com sucesso!'})


@app.route("/curso/<curso_id>", methods=['PUT'])
def update_curso(curso_id=None):
    request_data = request.get_json()
    nome = request_data['nome']
    carga_horaria = request_data['carga_horaria']

    mongo.db.cursos.update_one(
        {"id": curso_id},
        {
            "$set": {
                "nome": request_data['nome'],
                "carga_horaria": request_data['carga_horaria']
            }
        }
    )

    return jsonify({"message": "Curso atualizado com sucesso!"})


@app.route("/curso/<curso_id>", methods=['DELETE'])
def delete_curso(curso_id=None):
    mongo.db.cursos.remove({'id': curso_id})

    cursos = mongo.db.cursos
    curso_obj = cursos.find_one({'id': curso_id})
    if curso_obj is not None:
        retorno = "Erro ao excluir curso"
    else:
        retorno = "Curso excluido com sucesso"
    return jsonify({'mensagem': retorno})


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

    return jsonify({'result': 'matriculado!', "id": id})


@app.route("/matricula/<matricula_id>", methods=['DELETE'])
def delete_matricula(matricula_id):
    mongo.db.matriculas.remove({'id': matricula_id})

    matriculas = mongo.db.matriculas
    matricula_obj = matriculas.find_one({'id': matricula_id})
    if matricula_obj != None:
        retorno = "Error"
    else:
        retorno = "matricula excluido"
    return jsonify({'mensagem': retorno})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
