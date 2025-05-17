from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app import db
from app.models import users

bp = Blueprint('register', __name__)

@bp.route('', methods=['POST', 'OPTIONS'])
@bp.route('/', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        response = jsonify({})  # Return an empty JSON object
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200

    #  POST logic
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if users.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    password_hash = generate_password_hash(password)
    user = users(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201
