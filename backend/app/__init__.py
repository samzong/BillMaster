import os
import logging
from flask import Flask
from app.config.config import config

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """应用工厂"""
    logger.info("=== 创建 Flask 应用 ===")
    
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    logger.info(f"使用配置: {config_name}")
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    logger.debug(f"应用配置: {app.config}")
    
    # 初始化扩展
    logger.info("初始化扩展")
    from app.extensions import init_extensions
    init_extensions(app)
    
    # 注册蓝图
    logger.info("注册蓝图")
    from app.api.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    logger.info("应用创建完成")
    return app 