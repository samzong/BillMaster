from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app('development')

def init_db():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 创建管理员用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password='password',
                email='admin@example.com'
            )
            db.session.add(admin)
            db.session.commit()
            print('Created admin user')
        else:
            print('Admin user already exists')

if __name__ == '__main__':
    init_db() 