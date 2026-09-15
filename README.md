# User Authentication System

A full-stack user authentication system built with React.js, Python Flask, and SQLite.

## Features

- User registration
- User login
- Password validation
- Secure password hashing with bcrypt
- Duplicate username and email validation
- SQLite database
- REST API
- Login success dashboard
- Logout
- React state management
- CORS support

## Tech Stack

### Frontend
- React.js
- Vite
- JavaScript
- HTML
- CSS

### Backend
- Python
- Flask
- Flask-CORS
- Flask-Bcrypt

### Database
- SQLite

## Project Structure

```text
user-authentication-system/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
├── backend/
│   ├── app.py
│   └── requirements.txt
├── .gitignore
└── README.md
```

## Setup

### 1. Backend

Open a terminal inside the `backend` folder.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```cmd
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
python app.py
```

The backend runs on:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/api/health
```

### 2. Frontend

Open another terminal inside the `frontend` folder.

Install dependencies:

```bash
npm install
```

Run the frontend:

```bash
npm run dev
```

The frontend runs on:

```text
http://localhost:5173
```

## API Endpoints

### Health Check

```text
GET /api/health
```

### Register

```text
POST /api/register
```

Request:

```json
{
  "username": "fazil",
  "email": "fazil@example.com",
  "password": "123456"
}
```

### Login

```text
POST /api/login
```

Request:

```json
{
  "username": "fazil",
  "password": "123456"
}
```

## Authentication Flow

```text
React Frontend
      |
      | HTTP Request
      v
Flask REST API
      |
      v
SQLite Database
      |
      v
bcrypt Password Verification
      |
      v
JSON Response
      |
      v
React UI
```

## Running the Project

Run the backend and frontend in separate terminals.

Backend:

```bash
cd backend
venv\Scripts\activate
python app.py
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```
