# Blueprint organizes all the routes
# jsonify converts dictionaries into JSON
from flask import Blueprint, jsonify, request
from pydantic import ValidationError # to validate our models using pydantic
from app.models.user import LoginPayload
from app.models.products import *
from app import db
from bson import ObjectId

main_bp = Blueprint('main_bp', __name__)

# RF: O sistema deve permitir que um usuário se autentique para obter um token
# HTTP POST METHOD
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_json() # reads the body (JSON) and returns a dictionary
        # the ** operator transforms the dictionary (raw_data) into data for the attributes (uncouple)
        user_login = LoginPayload(**raw_data).model_dump()

    except ValidationError as error:
        return jsonify({'error': error.errors()}), 400 # http status_code
    except Exception as e: # for any other inconsistency
        return jsonify({'error': 'Error in the request'}), 500
    
    if user_login['username'] == 'admin' and user_login['password'] == '12345':
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Wrong username or password'})
    
    # model_dump_json transforms the dictionary back to a json
    # return jsonify({'message': f'Route to login the user {user_login.model_dump_json()}'})

# RF: O sistema deve permitir listagem de todos os produtos
# HTTP GET METHOD (default)
@main_bp.route('/products')
def get_products():
    products_cursor = db.products.find({}) # retrieve all products in the database
    products_list = [ProductDBModel(**product).model_dump(by_alias= True, exclude_none = True) for product in products_cursor]

    # for product in products_cursor:
    #     product['_id'] = str(product['_id']) # converts the product['_id'] into string
    #     products_list.append(product)

    return jsonify(products_list)
    # return jsonify({'message': 'Route to list all products'})

# RF: O sistema deve permitir a criação de um novo produto
@main_bp.route('/products', methods=['POST'])
def create_products():
    return jsonify({'message': 'Route to create a product'})

# RF: O sistema deve permitir a visualização dos detalhes de um produto
@main_bp.route('/product/<string:product_id>')
def get_product_by_id(product_id):

    try:
        oid = ObjectId(product_id)
    except Exception as error:
        return jsonify({'error': f'Error while converting the {product_id} into ObjectId: {error}'})

    product = db.products.find_one({'_id': oid})
    
    if product:
        product['_id'] = str(product['_id'])
        return jsonify(product)
    else:
        return jsonify({'error': f'Product {product_id} not found'})

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