from app.models import Produto
from app import db

def criar_produto(nome, descricao, preco, quantidade):
    produto = Produto(nome=nome, descricao=descricao, preco=preco, quantidade=quantidade)
    db.session.add(produto)
    db.session.commit()
    return produto

def listar_produtos():
    return Produto.query.all()