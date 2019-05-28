import pymongo
from pymongo import MongoClient

DATABASE = "db_contatos"


class DBHelper:
    
    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client(DATABASE)

    def get_contato(self, nome):
        return self.db.contato.find_one({"nome": nome})

    def add_contato(self, nome, canal, valor, obs):
        return self.db.contato.insert({"nome": nome, "canal": canal, "valor": valor, "obs": obs})

    def remove_contato(self, id):
        return self.db.contato.remove({"id": id})

    def add_table(self, nome, canal, valor, obs):
        new_id = self.db.tables.insert(
            {"nome": nome, "canal": canal, "valor": valor, "obs": obs})
