from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "user-authentication-system-secret-key"
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
DATABASE = "users.db"

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_db()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

@app.route("/api/health")
def health():
    return jsonify({"message": "Backend is running"})

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    if not username or not email or not password:
        return jsonify({"message": "Please fill all fields"}), 400
    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400
    connection = get_db()
    existing = connection.execute(
        "SELECT id FROM users WHERE username = ? OR email = ?",
        (username, email)
    ).fetchone()
    if existing:
        connection.close()
        return jsonify({"message": "Username or email already exists"}), 409
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    connection.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, hashed_password)
    )
    connection.commit()
    connection.close()
    return jsonify({"message": "Registration successful"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    if not username or not password:
        return jsonify({"message": "Please fill all fields"}), 400
    connection = get_db()
    user = connection.execute(
        "SELECT id, username, email, password FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    connection.close()
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid username or password"}), 401
    session["user_id"] = user["id"]
    return jsonify({
        "message": "Login successful",
        "user": {"id": user["id"], "username": user["username"], "email": user["email"]}
    })

@app.route("/api/me")
def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "Not authenticated"}), 401
    connection = get_db()
    user = connection.execute(
        "SELECT id, username, email FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    connection.close()
    if not user:
        session.clear()
        return jsonify({"message": "Not authenticated"}), 401
    return jsonify({
        "user": {"id": user["id"], "username": user["username"], "email": user["email"]}
    })

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
