
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models import users  # Assuming your User model is in app.models

bp = Blueprint('login', __name__)

@bp.route('', methods=['POST', 'OPTIONS'])
@bp.route('/', methods=['POST', 'OPTIONS'])
def login():
    """
    Handles user login.  Accepts username and password_hash, checks
    credentials, and returns a token on success.  Includes detailed logging.
    """

    if request.method == 'OPTIONS':
        # Handle OPTIONS requests (for CORS)
        response = jsonify({})  # Return an empty JSON object
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 200

    #  POST logic
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    username = data.get('username')
    password = data.get('password_hash')
    if not username or not password:

        return jsonify({'error': 'Username and password required'}), 400
    try:
        user = users.query.filter_by(username=username).first()
    except Exception as e:
        return jsonify({'error': 'Database error'}), 500  # Internal Server Error
    if user and check_password_hash(user.password_hash, password):
        # In production, generate a JWT or session token here
        token = 'dummy_token'  # Replace with actual token generation
        return jsonify({'token': token, 'username': user.username}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401
