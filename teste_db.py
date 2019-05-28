from dao.database import DBHelper
from models.contato import Contato

db = DBHelper()
contato = Contato()
db.add_contato("teste", "email", "contato@teste.com", "teste")
