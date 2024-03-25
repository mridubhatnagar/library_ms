from flask import Flask
from app.extensions import db
from app.extensions import migrate 
from config import Config
from app.models.books import Books
from app.models.members import Members
from app.models.transactions import Transactions
from app.models.payments import Payments

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app,db)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.books import bp as books_bp
    app.register_blueprint(books_bp, url_prefix='/books')
    from app.members import bp as members_bp
    app.register_blueprint(members_bp, url_prefix='/members')
    from app.payments import bp as payments_bp
    app.register_blueprint(payments_bp, url_prefix='/payments')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app