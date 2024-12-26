import logging
from app import create_app

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = create_app('development')

if __name__ == '__main__':
    # 添加启动日志
    logging.info("=== 启动 Flask 应用 ===")
    logging.info(f"调试模式: {app.debug}")
    logging.info(f"应用配置: {app.config}")
    
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True
    ) 