from flask import Blueprint, jsonify, request
from app.models import Cliente
from app import db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'contato': p.contato,
        'cpf': p.cpf
    } for p in clientes])

@clientes_bp.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    data = request.get_json()
    novo_cliente = Cliente(
        nome=data['nome'],
        contato=data['contato'],
        cpf=data['cpf']
    )
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente cadastrado com sucesso!'}), 201