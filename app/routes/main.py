# Blueprint organizes all the routes
# jsonify converts dictionaries into JSON
from flask import Blueprint, jsonify

main_bp = Blueprint('main_bp', __name__)

# RF: O sistema deve permitir que um usuário se autentique para obter um token
# HTTP POST METHOD
@main_bp.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'Route to login'})

# RF: O sistema deve permitir listagem de todos os produtos
# HTTP GET METHOD (default)
@main_bp.route('/products')
def get_products():
    return jsonify({'message': 'Route to list all products'})

# RF: O sistema deve permitir a criação de um novo produto
@main_bp.route('/products', methods=['POST'])
def create_products():
    return jsonify({'message': 'Route to create a product'})

# RF: O sistema deve permitir a visualização dos detalhes de um produto
@main_bp.route('/product/<int:product_id>')
def get_product_by_id(product_id):
    return jsonify({'message': 'Route to list the details of the product'})

# RF: O sistema deve permitir a atualização de um único produto e produto existente
@main_bp.route('/product/<int:product_id>', methods=['PUT'])
def update_product_by_id(product_id):
    return jsonify({'message': 'Route to update the details of the product'})

# RF: O sistema deve permitir a exclusão de um único produto e produto existente
@main_bp.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product_by_id(product_id):
    return jsonify({'message': 'Route to delte the product'})

# RF: O sistema deve permitir a importação de vendas através de um arquivo
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({'message': 'Route to upload the sales'})

@main_bp.route('/')
def index():
    return jsonify({'message': 'Welcome to the StyleSync!'})



