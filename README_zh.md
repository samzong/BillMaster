# BillMaster 账单管理系统

一个使用 Flask 和 Vue.js 构建的现代化账单管理系统，具有用户认证和个人中心功能。

[English Documentation](./README.md)

## 功能特点

- 基于 JWT 的用户认证
- 用户个人中心管理
- 密码修改功能
- 使用 Element Plus 构建的现代化响应式界面
- 基于 Flask 的 RESTful API
- 使用 SQLAlchemy ORM 的 SQLite 数据库
- 跨域支持
- TypeScript 支持
- 完善的错误处理
- 详细的日志记录

## 技术栈

### 后端
- Python 3.12+
- Flask 3.0.0
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Marshmallow

### 前端
- Vue 3.3+
- TypeScript
- Vite
- Pinia
- Vue Router
- Element Plus
- Axios

## 快速开始

### 环境要求
- Python 3.12 或更高版本
- Node.js 16 或更高版本
- npm 或 yarn

### 后端设置
1. 创建并激活虚拟环境：
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows 系统：venv\Scripts\activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 初始化数据库：
```bash
python init_db.py
```

4. 启动后端服务器：
```bash
python run.py
```

后端服务器将在 http://localhost:5000 启动

### 前端设置
1. 安装依赖：
```bash
cd frontend
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

前端开发服务器将在 http://localhost:3000 启动

### 初始登录信息
- 用户名：admin
- 密码：password

## 项目结构

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── utils/
│   │   └── config/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── views/
│   │   └── router/
│   └── package.json
└── README.md
```

## API 文档

### 认证接口
- POST `/api/auth/login`: 用户登录
- GET `/api/auth/profile`: 获取用户信息
- POST `/api/auth/change-password`: 修改密码

## 参与贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加一些很棒的特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情。 