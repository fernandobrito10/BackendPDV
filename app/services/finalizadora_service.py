from app.models import Finalizadora
from app import db

def criar_finalizadora(descricao):
    finalizadora = Finalizadora(descricao=descricao)
    db.session.add(finalizadora)
    db.session.commit()
    return finalizadora

def listar_finalizadoras():
    return Finalizadora.query.all()