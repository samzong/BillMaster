import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from marshmallow import ValidationError

from ..models.user import User
from ..extensions import db
from ..schemas.user import UserSchema, UserLoginSchema, ChangePasswordSchema

# 配置日志
logger = logging.getLogger(__name__)

# 创建蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        # 验证请求数据
        schema = UserLoginSchema()
        data = schema.load(request.get_json())
        
        # 查找用户
        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            logger.warning(f"登录失败: 用户名或密码错误 (username: {data['username']})")
            return jsonify({"message": "用户名或密码错误"}), 401
        
        # 创建访问令牌
        access_token = create_access_token(identity=str(user.id))
        
        # 返回用户信息和令牌
        return jsonify({
            "access_token": access_token,
            "user": UserSchema().dump(user)
        })
        
    except ValidationError as e:
        logger.error(f"登录数据验证失败: {e.messages}")
        return jsonify({"message": "数据验证失败", "errors": e.messages}), 400
    except Exception as e:
        logger.error(f"登录过程出错: {str(e)}")
        return jsonify({"message": "服务器错误"}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户信息"""
    try:
        # 获取当前用户ID
        user_id = get_jwt_identity()
        if not user_id:
            logger.error("获取用户信息失败: 无法获取用户ID")
            return jsonify({"message": "无法获取用户信息"}), 401
        
        # 查找用户
        user = User.query.get(int(user_id))
        if not user:
            logger.error(f"获取用户信息失败: 未找到用户 (id: {user_id})")
            return jsonify({"message": "用户不存在"}), 404
        
        # 返回用户信息
        return jsonify(UserSchema().dump(user))
        
    except Exception as e:
        logger.error(f"获取用户信息时出错: {str(e)}")
        return jsonify({"message": "服务器错误"}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """修改密码"""
    try:
        # 验证请求数据
        schema = ChangePasswordSchema()
        data = schema.load(request.get_json())
        
        # 获取当前用户
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            logger.error(f"修改密码失败: 未找到用户 (id: {user_id})")
            return jsonify({"message": "用户不存在"}), 404
        
        # 验证原密码
        if not user.check_password(data['old_password']):
            logger.warning(f"修改密码失败: 原密码错误 (id: {user_id})")
            return jsonify({"message": "原密码错误"}), 400
        
        # 更新密码
        user.set_password(data['new_password'])
        db.session.commit()
        
        logger.info(f"密码修改成功 (id: {user_id})")
        return jsonify({"message": "密码修改成功"})
        
    except ValidationError as e:
        logger.error(f"修改密码数据验证失败: {e.messages}")
        return jsonify({"message": "数据验证失败", "errors": e.messages}), 400
    except Exception as e:
        logger.error(f"修改密码时出错: {str(e)}")
        return jsonify({"message": "服务器错误"}), 500 