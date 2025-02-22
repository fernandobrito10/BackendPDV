from app.models import Produto
from app import db

def criar_produto(descricao, descricao_reduzida, preco, unidade, quantidade, codigo_ean, fornecedor_id, fornecedor_nome):
    produto = Produto(descricao=descricao, descricao_reduzida=descricao_reduzida, preco=preco, unidade=unidade, quantidade=quantidade, codigo_ean=codigo_ean, fornecedor_id=fornecedor_id, fornecedor_nome=fornecedor_nome)
    db.session.add(produto)
    db.session.commit()
    return produto

def listar_produtos():
    return Produto.query.all()