from flask import Flask
from pymongo import MongoClient
from .routes.category_routes import category_bp

db = None

# application factory (contains the application settings)
def create_app():
    app = Flask(__name__)
    # app.register_blueprint(category_bp)
    app.config.from_object('config.Config') # from_object('file.class')

    global db # indicates we are changing the db variable and not creating another one

    # connects to the database
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()
    except Exception as error:
        print(f'Error while connecting to the database: {error}')

    # import the blueprints in the factory and not in the module
    from .routes.main import main_bp
    
    app.register_blueprint(main_bp) # register the blueprint as the main_bp object
 
    return app