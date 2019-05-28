import pymongo
from flask import Flask
from flask import jsonify
from flask import request
from models.contato import Contato
from dao.db import db

app = Flask(__name__)


# BASE_URL = "/api/components/schemas"
BASE_URL = "/api"

contato_1 = Contato('1', 'teste', 'email', 'teste1@teste.com', 'Email teste1')
contato_2 = Contato('2', 'teste2', 'email', 'teste2@teste.com', 'Email teste2')
contato_3 = Contato('3', 'teste3', 'email', 'teste3@teste.com', 'Email teste3')
contato_4 = Contato('4', 'teste4', 'email', 'teste4@teste.com', 'Email teste4')


contatos = [contato_1, contato_2, contato_3, contato_4]
messages = {
    "empty": {"message": "Dados vazios"},
    "none": {"message": "Contato nao encontrado!"},
    "created": {"message": "Contato criado com sucesso!"},
    "updated": {"message": "Contato atualizado com sucesso!"},
    "deleted": {"message": "Contato removido com sucesso!"}
}


@app.route(BASE_URL)
def index():
    return "Hello World"


@app.route(BASE_URL + "/Contato", methods=['GET'])
def get_contatos():
    print(len(contatos))
    if len(contatos) > 0:
        return jsonify(ContatoSchema(many=True).dump(contatos))
    return jsonify(messages["empty"])


@app.route(BASE_URL + "/Contato/<contato_id>", methods=['GET'])
def get_contato(contato_id=None):
    print(contato_id)
    for contato in contatos:
        if contato.id == contato_id:
            return jsonify(ContatoSchema().dump(contato))

    return jsonify(messages["empty"])


@app.route(BASE_URL + "/ContatoCreate", methods=['POST'])
def create_contato():
    request_data = request.get_json()
    new_contato = Contato(str(len(contatos) + 1), request_data['nome'], request_data['canal'],
                          request_data['valor'], request_data['obs'])
    contatos.append(new_contato)
    return jsonify(messages["created"])


@app.route(BASE_URL + "/ContatoUpdate/<contato_id>", methods=['PUT'])
def update_contato(contato_id=None):
    request_data = request.get_json()
    for contato in contatos:
        if contato.id == contato_id:
            contato.nome = request_data['nome']
            contato.canal = request_data['canal']
            contato.valor = request_data['valor']
            contato.obs = request_data['obs']
            return jsonify(messages["updated"])
    return jsonify(messages["empty"])


@app.route(BASE_URL + "/Contato/<contato_id>", methods=['DELETE'])
def delete_contato(contato_id=None):
    for contato in contatos:
        if contato.id == contato_id:
            print(contatos.index(contato))
            contatos.pop()
            return jsonify(messages["deleted"])
        else:
            return jsonify(messages["none"])


if __name__ == '__main__':
    app.run(port=5000, debug=True)
