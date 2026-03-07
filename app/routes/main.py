from flask import Blueprint, jsonify

# Blueprint organizes all the routes
# jsonify converts dictionaries into JSON

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return jsonify({'message': 'Welcome to the StyleSync!'})

# HTTP GET METHOD (default)
@main_bp.route('/products')
def get_products():
    return jsonify({'message': 'Route to list all products'})

# HTTP POST METHOD
@main_bp.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'Route to login'})