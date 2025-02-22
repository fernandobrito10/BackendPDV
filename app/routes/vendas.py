from flask import Blueprint, jsonify, request
from app.models import Venda, Produto, Cliente, Finalizadora, ItemVenda
from app import db
from datetime import datetime

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/pdv', methods=['POST'])
def realizar_venda():
    data = request.get_json()
    total_venda = 0.0

    # Verificar cliente apenas se um ID foi fornecido
    cliente = None
    if data.get('cliente_id'):
        cliente = Cliente.query.get(data.get('cliente_id'))
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado!'}), 404
    
    finalizadora = Finalizadora.query.get(data.get('finalizadora_id'))
    if not finalizadora:
        return jsonify({'erro': 'Finalizadora não encontrada!'}), 404

    nova_venda = Venda(
        cliente_id = cliente.id if cliente else None,
        finalizadora_id = finalizadora.id,
        vendedor = data.get('vendedor'),
        data=datetime.utcnow(),
        total=0.0
    )

    try:
        for item in data.get('itens', []):
            produto = Produto.query.get(item['produto_id'])
            if not produto:
                raise ValueError(f'Produto ID {item["produto_id"]} não encontrado!')
            
            novo_item = ItemVenda(
                produto_id=produto.id,
                preco_unitario=produto.preco,
                quantidade=item['quantidade']
            )
            total_venda += produto.preco * item['quantidade']
            nova_venda.itens.append(novo_item)
            produto.quantidade -= item['quantidade']  # Ainda atualiza o estoque, mas permite negativo

        nova_venda.total = total_venda
        db.session.add(nova_venda)
        db.session.commit()

        return jsonify({'mensagem': 'Venda registrada com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao registrar venda: {e}'}), 500

@vendas_bp.route('/vendas', methods=['GET'])
def listar_vendas():
    vendas = Venda.query.options(
        db.joinedload(Venda.itens).joinedload(ItemVenda.produto),
        db.joinedload(Venda.cliente),
        db.joinedload(Venda.finalizadora)
    ).all()

    resultado = []
    for venda in vendas:
        venda_data = {
            'venda_id': venda.id,
            'total': venda.total,
            'cliente': venda.cliente.nome if venda.cliente else "Venda Avulsa",
            'finalizadora': venda.finalizadora.descricao,
            'itens': [{
                'produto': item.produto.descricao,
                'preco_unitario': item.preco_unitario,
                'quantidade': item.quantidade,
                'subtotal': item.preco_unitario * item.quantidade
            } for item in venda.itens]
        }
        resultado.append(venda_data)

    return jsonify(resultado), 200