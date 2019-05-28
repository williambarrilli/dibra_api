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


app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)
# BASE_URL = "/api/components/schemas"
# BASE_URL = "/api"

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


@app.route("/aluno", methods=['GET'])
def get_all_alunos():
    alunos = mongo.db.alunos
    retorno = []
    for aluno_obj in alunos.find():
        retorno.append(
            {'id': aluno_obj['id'], 'name': aluno_obj['name'], 'canal': aluno_obj['canal'], 'valor': aluno_obj['valor'], 'obs': aluno_obj['obs']})
        if len(retorno) == 0:
            return jsonify({"message": "Não há alunos cadastrados!"})

    return jsonify({'alunos': retorno})



@app.route("/aluno/<aluno_id>", methods=['GET'])
def get_aluno(aluno_id=None):
    alunos = mongo.db.alunos
    aluno_obj = alunos.find_one({'name': name})
    if not aluno_obj:
        retorno = "aluno não encontrado"
        return jsonify(retorno)
    aluno_obj.pop('_id')
    return jsonify(aluno_obj)
    

@app.route("/aluno", methods=['POST'])
def create_aluno():
    alunos = mongo.db.alunos
    name = request.json['name']
    canal = request.json['canal']
    valor = request.json['valor']
    obs = request.json['obs']
    id = gera_id()

    alunos.insert({
        'id': id,
        'name': name,
        'canal': canal,
        'valor': valor,
        'obs': obs})

    return jsonify({'result': 'ok'})


@app.route("/aluno/<aluno_id>", methods=['PUT'])
def set_aluno_name(aluno_id):
    request_data = request.get_json()   
    new_name = request_data['name']
    canal = request_data['canal']
    valor = request_data['valor']
    obs = request_data['obs']
    mongo.db.alunos.update_one(
        {"name": name},
        {
            "$set": {
                "name": new_name,
                "canal": canal,
                "valor": valor,
                "obs": obs
            }
        }
    )
    
    return jsonify({"message": "Só por Deus"})

@app.route("/aluno/<aluno_id>", methods=['DELETE'])
def delete_aluno(aluno_id):
    mongo.db.alunos.remove({'name': name})

    alunos = mongo.db.alunos
    aluno_obj = alunos.find_one({'name': name})
    if aluno_obj != None:
        retorno = "Error"
    else:
        retorno = "aluno excluido"
    return jsonify({'mensagem': retorno})




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
