from app import db
from datetime import datetime

class Produto(db.Model):
    __table_args__ = (
        db.Index('idx_produto_descricao', 'descricao'),
        db.Index('idx_produto_id', 'id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    descricao_reduzida = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.Text, nullable=False)
    quantidade = db.Column(db.Float, nullable=True)
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
    __table_args__ = (
        db.Index('idx_venda_data', 'data'),
        db.Index('idx_venda_cliente', 'cliente_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)
    finalizadora_id = db.Column(db.Integer, db.ForeignKey('finalizadora.id'), nullable=False)
    vendedor = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=True)
    data = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    total = db.Column(db.Float, nullable=False, default=0.0)

    cliente = db.relationship('Cliente', backref='vendas')
    finalizadora = db.relationship('Finalizadora', backref='vendas')
    itens = db.relationship('ItemVenda', backref='vendas', cascade='all, delete-orphan')


class ItemVenda(db.Model):
    __table_args__ = (
        db.Index('idx_itemvenda_venda', 'venda_id'),
        db.Index('idx_itemvenda_produto', 'produto_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Float, nullable=False)

    produto = db.relationship('Produto', backref='itens_venda')

class MovimentacaoEstoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)