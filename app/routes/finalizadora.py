from flask import Blueprint, jsonify, request
from app.models import Finalizadora
from app import db

finalizadoras_bp = Blueprint('finalizadoras', __name__)

@finalizadoras_bp.route('/finalizadoras', methods=['GET'])
def listar_finalizadoras():
    finalizadoras = Finalizadora.query.all()
    return jsonify([{
        'id': p.id,
        'descricao': p.descricao,
    } for p in finalizadoras])

@finalizadoras_bp.route('/finalizadoras', methods=['POST'])
def criar_finalizadora():
    data = request.get_json()
    nova_finalizadora = Finalizadora(
        descricao=data['descricao']
    )
    db.session.add(nova_finalizadora)
    db.session.commit()
    return jsonify({'message': 'Finalizadora criada com sucesso!'}), 201