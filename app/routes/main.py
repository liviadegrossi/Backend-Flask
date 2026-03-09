# Blueprint organizes all the routes
# jsonify converts dictionaries into JSON
from flask import Blueprint, jsonify, request, current_app
from pydantic import ValidationError # to validate our models using pydantic
from app.models.user import LoginPayload
from app.models.products import *
from app import db
from bson import ObjectId
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt

main_bp = Blueprint('main_bp', __name__)

# checks user's credentials and returns a token
@main_bp.route('/login', methods=['POST'])
def login(): 
    # reads user's credentials and validates against the model in the Payload class
    try:
        raw_data = request.get_json() # reads the body (JSON) and returns a dictionary
        # the ** operator transforms the dictionary (raw_data) into data for the attributes (uncouple)
        user_login = LoginPayload(**raw_data)
    except ValidationError as error:
        return jsonify({'error': error.errors()}), 400 # http status_code
    except Exception as e: # for any other inconsistency
        return jsonify({'error': f'Error in the request: {e}'}), 500
    
    # whether user's credentials are the expected ones, generates a token, and returns it
    if user_login.username == 'admin' and user_login.password == '12345':
        token = jwt.encode(
            {
                "user_id": user_login.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30) # each token is valid for 30 minutes
            },
            str(current_app.config['SECRET_KEY']),
            algorithm='HS256'
        )
        return jsonify({'access_token': token}), 200
    
    return jsonify({'message': 'Wrong username or password'}), 401

# lists all products
@main_bp.route('/products')
def get_products():
    products_cursor = db.products.find({}) # retrieve all products in the database
    products_list = [ProductDBModel(**product).model_dump(by_alias= True, exclude_none = True) for product in products_cursor]

    # for product in products_cursor:
    #     product['_id'] = str(product['_id']) # converts the product['_id'] into string
    #     products_list.append(product)

    return jsonify(products_list)

# RF: O sistema deve permitir a criação de um novo produto
@token_required
@main_bp.route('/products', methods=['POST'])
def create_products():
    try:
        product = Product(**request.get_json())
    except ValidationError as error:
        return jsonify({'error': error.errors()})
    
    create_product_result = db.products.insert_one(product.model_dump())

    return jsonify({'message': f'Product created successfully with id: {str(create_product_result.inserted_id)}'}), 201 # status_code 201 = created

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

# Update a product using its id
@token_required
@main_bp.route('/product/<string:product_id>', methods=['PUT'])
def update_product_by_id(product_id):
    
    # validates the data received in the request
    try:
        oid = ObjectId(product_id)
        update_data = UpdateProduct(**request.get_json())
    except ValidationError as error:
        return jsonify({'error': error.errors()})
    
    update_result = db.products.update_one(
        {"_id": oid},
        {"$set": update_data.model_dump(exclude_unset=True)}
    )

    # checks if the data was updated
    if update_result.matched_count == 0:
        return jsonify({"error": "Product not found"}), 404
    
    update_product = db.products.find_one({"_id": oid})  # returns a dictionary
    return jsonify(ProductDBModel(**update_product).model_dump(by_alias=True, exclude=None)) # converts the dict into a JSON before returning it

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