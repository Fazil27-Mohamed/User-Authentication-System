# User Authentication System

A full-stack user authentication system built with React.js, Flask, and SQLite.

## Features

- User registration and login
- Secure bcrypt password hashing
- SQLite database
- Flask session management
- Dashboard after successful login
- Logout functionality
- React and Flask API integration
- Responsive interface

## Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend: `http://127.0.0.1:5000`

### Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

## API

- GET `/api/health`
- POST `/api/register`
- POST `/api/login`
- GET `/api/me`
- POST `/api/logout`
