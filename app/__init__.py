from flask import Flask
from .config import Config
from .extensions import db, login_manager, migrate, csrf
from .models import User  # Importamos para que SQLAlchemy lo conozca

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        print('Base de datos inicializada.')

    # Configurar login_manager
    login_manager.login_view = 'auth.login'  # nombre de la función de login
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar blueprints
    from .main import main_bp
    from .auth import auth_bp
    from .dashboard import dashboard_bp
    from .nutritionist import nutritionist_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(nutritionist_bp, url_prefix='/nutritionist')

    return app