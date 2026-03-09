from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.user import *
from app import db
from bson import ObjectId
from app.decorators import token_required

user_bp = Blueprint('user_bp', __name__)

# Retrieve all users in the database
@token_required
@user_bp.route('/users')
def get_users():

    # retrieve all users in the database
    users_cursor = db.users.find({})

    # for each user, converts it from a dictionary into a json
    users_list = [UserDBModel(**user).model_dump(by_alias=True, exclude_none=True) for user in users_cursor]

    return jsonify(users_list)

# Create a user
@token_required
@user_bp.route('/user', methods=['POST'])
def create_user():

    # validates the data received in the request
    try:
        user_data = LoginPayload(**request.get_json()).model_dump() # creates an unecessary id attribute
    except ValidationError as error:
        return jsonify({'error': error.errors()})

    create_user_result = db.users.insert_one(user_data)

    return jsonify({'message': f'User created successfully with ID: {str(create_user_result.inserted_id)}'}), 201

# Delete a user using its id
@token_required
@user_bp.route('/user/<string:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):

    # validates the id received
    try:
        oid = ObjectId(user_id)
    except ValidationError as error:
        return jsonify({'error': 'Invalid user id'}), 400
    
    # Attempt to delete the user
    delete_user_result = db.users.delete_one({'_id': oid})

    if delete_user_result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404
    
    return '', 204
