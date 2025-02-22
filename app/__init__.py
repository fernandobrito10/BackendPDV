from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.produtos import produtos_bp
    from app.routes.estoque import estoque_bp
    from app.routes.vendas import vendas_bp
    from app.routes.cliente import clientes_bp
    from app.routes.finalizadora import finalizadoras_bp

    app.register_blueprint(produtos_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(vendas_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(finalizadoras_bp)

    return app