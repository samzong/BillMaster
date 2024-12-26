import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# 配置日志
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def init_extensions(app):
    """初始化所有扩展"""
    logger.info("初始化 SQLAlchemy")
    db.init_app(app)
    
    logger.info("初始化 Migrate")
    migrate.init_app(app, db)
    
    logger.info("初始化 JWT")
    jwt.init_app(app)
    
    # JWT 错误处理
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        logger.error(f"无效的 token: {error}")
        return {"message": "无效的认证令牌"}, 401
        
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        logger.error(f"未提供 token: {error}")
        return {"message": "未提供认证令牌"}, 401
        
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        logger.error(f"token 已过期: {jwt_data}")
        return {"message": "认证令牌已过期"}, 401
    
    # 配置 CORS
    logger.info("配置 CORS")
    CORS(app, resources={
        r"/api/*": {  # 只对 /api 路径启用 CORS
            "origins": ["http://localhost:3000"],  # 只允许前端域名
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    logger.info("所有扩展初始化完成")