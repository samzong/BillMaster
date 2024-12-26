from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from app import db
from app.models import User
from config import Config
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token.split()[1], Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and user.check_password(data.get('password')):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        }, Config.JWT_SECRET_KEY)
        
        return jsonify({
            'token': token,
            'username': user.username
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/api/change_password', methods=['POST'])
@token_required
def change_password(current_user):
    data = request.get_json()
    if current_user.check_password(data.get('old_password')):
        current_user.set_password(data.get('new_password'))
        db.session.commit()
        return jsonify({'message': 'Password updated successfully'})
    return jsonify({'message': 'Invalid old password'}), 400 