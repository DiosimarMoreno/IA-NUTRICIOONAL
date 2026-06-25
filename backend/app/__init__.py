from flask import Flask

def create_app():
    
    app = Flask(__name__,
        template_folder="../../frontend",
        static_folder="../../frontend/css"
        )

    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app