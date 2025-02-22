from flask import Blueprint, jsonify, request
from app.models import Produto
from app import db

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.with_entities(
        Produto.id,
        Produto.descricao,
        Produto.preco
    ).all()
    
    return jsonify([{
        'id': p.id,
        'descricao': p.descricao,
        'preco': p.preco,
    } for p in produtos])

@produtos_bp.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()
    novo_produto = Produto(
        descricao=data['descricao'],
        descricao_reduzida=data['descricao_reduzida'],
        preco=data['preco'],
        unidade=data['unidade'],
        quantidade=data['quantidade'],
        codigo_ean=data['codigo_ean'],
        fornecedor_id=data['fornecedor_id'],
        fornecedor_nome=data['fornecedor_nome']
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({'message': 'Produto criado com sucesso!'}), 201