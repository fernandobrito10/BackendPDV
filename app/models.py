from app import db
from datetime import datetime

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    descricao_reduzida = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.Text, nullable=False)
    quantidade = db.Column(db.Integer, nullable=True)
    codigo_ean = db.Column(db.Integer, nullable=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=True)
    fornecedor_nome = db.Column(db.String, db.ForeignKey('fornecedor.razao_social'), nullable=True)

class Finalizadora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(20), nullable=False)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(100), nullable=False)
    nome_fantasia = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(100), nullable=True)
    cpf = db.Column(db.String(11), nullable=True)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    finalizadora = db.Column(db.Integer, db.ForeignKey('finalizadora.id'), nullable=False)
    vendedor = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=True)
    produto = db.relationship('Produto', backref='vendas')

class MovimentacaoEstoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)