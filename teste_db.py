from dao.database import DBHelper
from models.aluno import Aluno

db = DBHelper()
aluno = Aluno()
db.add_aluno("teste", "email", "contato@teste.com", "teste")
