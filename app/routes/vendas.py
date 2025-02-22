from flask import Blueprint, jsonify, request
from app.models import Venda, Produto
from app import db
from app.routes.estoque import saida_estoque
from datetime import datetime

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/pdv', methods=['POST'])
def realizar_venda():
    data = request.get_json()
    
    produto = Produto.query.get(data['produto_id'])
    if not produto:
        return jsonify({'erro': 'Produto não encontrado!'}), 404
    
    if produto.quantidade < int(data['quantidade']):
        return jsonify({'erro': f'Estoque insuficiente. Disponível apenas {produto.quantidade}'}), 400

    try:
        nova_venda = Venda(
            produto_id=data['produto_id'],
            quantidade=data['quantidade'],
            finalizadora=data['finalizadora'],
            vendedor=data['vendedor'],
            data=datetime.utcnow()
        )
        produto.quantidade -= int(data['quantidade'])
        db.session.add(nova_venda)
        db.session.commit()
        return jsonify({'message': 'Venda feita com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao registrar venda: {e}'}), 500

@vendas_bp.route('/vendas', methods=['GET'])
def listar_vendas():
    vendas = db.session.query(
        Venda,
        Produto.descricao
    ).join(Produto).all()
    return jsonify([{
        'venda_id': v.id,
        'produto_id': v.produto_id,
        'produto_descricao': descricao,
        'quantidade': v.quantidade,
        'finalizadora': v.finalizadora,
        'vendedor': v.vendedor,
        'data': v.data.isoformat() if v.data else None
    } for v, descricao in vendas])