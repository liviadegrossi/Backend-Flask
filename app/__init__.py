from flask import Flask
from .routes.main import main_bp

def create_app():
    app = Flask(__name__)
    # register the blueprint as the main_bp object
    app.register_blueprint(main_bp)
    return app