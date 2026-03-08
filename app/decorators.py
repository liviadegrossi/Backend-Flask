from functools import wraps
from flask import request, jsonify, current_app
import jwt

# f is the function in which the decorator is used
def token_required(f):
    @wraps
    def decorated(*args, **kwargs): # guarantees any argument in the function

        token = None

        # check whether the 'Authorization' is part of the header
        if 'Authorization' in request.headers:
            auth_headers = request.headers['Authorization']

            # try to read the token
            try:
                token = auth_headers.split(' ')[1] # read the token
            except IndexError:
                return jsonify({'message': 'Malformed token'}), 401 # error 401 = unauthorized
        
        # whether there is no toke
        if not token:
            return jsonify({'error': 'Token not found'})
        
        # verifies whether the token is encrypted
        try:
            data_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['RS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Expired token'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(data_token, *args, **kwargs)

    return decorated   