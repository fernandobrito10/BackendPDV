from flask import Blueprint, jsonify, request
from app.models import Produto
from app import db

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        'id': p.id,
        'descricao': p.descricao,
        'descricao_reduzida': p.descricao_reduzida,
        'preco': p.preco,
        'unidade': p.unidade,
        'quantidade': p.quantidade,
        'codigo_ean': p.codigo_ean,
        'fornecedor_id': p.fornecedor_id,
        'fornecedor_nome': p.fornecedor_nome
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