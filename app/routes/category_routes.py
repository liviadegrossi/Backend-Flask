from flask import Blueprint, jsonify, request
from pydantic import ValidationError

category_bp = Blueprint('category_bp', __name__, url_prefix='categories')

@category_bp.route('/')
def get_categories():
    return jsonify({'message': 'Route to retrieve all categories'})

@category_bp.route('/', methods=['POST'])
def create_category():
    return jsonify({'message': 'Route to create a category'})

@category_bp.route('/<int:catego_id>', methods=['PUT'])
def update_category_by_id(category_id):
    return jsonify({'message': 'Route to update the attributes of a category'})

@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category_by_id(category_id):
    return jsonify({'message': 'Route to delete a category'})