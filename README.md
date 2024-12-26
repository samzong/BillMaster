# BillMaster

A modern billing management system built with Flask and Vue.js, featuring user authentication and profile management.

[中文文档](./README_zh.md)

## Features

- User authentication with JWT
- User profile management
- Password change functionality
- Modern and responsive UI with Element Plus
- RESTful API with Flask
- SQLite database with SQLAlchemy ORM
- CORS support
- TypeScript support
- Comprehensive error handling
- Detailed logging

## Tech Stack

### Backend
- Python 3.12+
- Flask 3.0.0
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Marshmallow

### Frontend
- Vue 3.3+
- TypeScript
- Vite
- Pinia
- Vue Router
- Element Plus
- Axios

## Getting Started

### Prerequisites
- Python 3.12 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup
1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize database:
```bash
python init_db.py
```

4. Start the backend server:
```bash
python run.py
```

The backend server will start at http://localhost:5000

### Frontend Setup
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend development server will start at http://localhost:3000

### Initial Login
- Username: admin
- Password: password

## Project Structure

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

## API Documentation

### Authentication Endpoints
- POST `/api/auth/login`: User login
- GET `/api/auth/profile`: Get user profile
- POST `/api/auth/change-password`: Change password

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 