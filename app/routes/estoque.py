from flask import Blueprint, jsonify, request
from app.models import Produto, db
from datetime import datetime

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/estoque/entrada', methods=['POST'])
def entrada_estoque():
    data = request.get_json()
    produto_id = data.get('produto_id')
    quantidade = data.get('quantidade')

    if not produto_id or not quantidade:
        return jsonify({'erro': 'Campos obrigatórios faltando: produto_id ou quantidade'}), 400

    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    produto.quantidade += quantidade
    db.session.commit()

    return jsonify({
        'mensagem': 'Entrada de estoque registrada',
        'produto': produto.descricao,
        'nova_quantidade': produto.quantidade
    }), 200

@estoque_bp.route('/estoque/saida', methods=['POST'])
def saida_estoque():
    data = request.get_json()
    produto_id = data.get('produto_id')
    quantidade = data.get('quantidade')

    if not produto_id or not quantidade:
        return jsonify({'erro': 'Campos obrigatórios faltando: produto_id ou quantidade'}), 400

    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    if produto.quantidade < quantidade:
        return jsonify({'erro': 'Quantidade insuficiente em estoque'}), 400

    produto.quantidade -= quantidade
    db.session.commit()

    return jsonify({
        'mensagem': 'Saída de estoque registrada',
        'produto': produto.descricao,
        'nova_quantidade': produto.quantidade
    }), 200

@estoque_bp.route('/estoque/relatorio', methods=['GET'])
def relatorio_estoque():
    produtos = Produto.query.all()
    relatorio = [{
        'id': p.id,
        'descricao': p.descricao,
        'quantidade': p.quantidade,
        'preco': p.preco
    } for p in produtos]

    return jsonify({'estoque': relatorio}), 200