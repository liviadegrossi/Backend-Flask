# application factory (contains the application settings)
from flask import Flask
from .routes.main import main_bp
from .routes.category_routes import category_bp
from pymongo import MongoClient

db = None

def create_app():
    app = Flask(__name__)
    # register the blueprint as the main_bp object
    app.register_blueprint(main_bp)
    app.register_blueprint(category_bp)
    app.config.from_object('config.Config') # from_object('file.class')

    global db # indicates we are changing the db variable and not creating another one

    # connects to the database
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()
    except Exception as error:
        print(f'Error while connecting to the database: {error}')

    return app