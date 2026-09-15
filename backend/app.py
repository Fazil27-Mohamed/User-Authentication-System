from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

DATABASE = "users.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()
    connection.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)"
    )
    connection.commit()
    connection.close()


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"message": "Authentication backend is running"})


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"message": "Please fill all fields"}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must contain at least 6 characters"}), 400

    connection = get_db()

    existing_user = connection.execute(
        "SELECT id FROM users WHERE username = ? OR email = ?",
        (username, email)
    ).fetchone()

    if existing_user:
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
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"message": "Please enter username and password"}), 400

    connection = get_db()

    user = connection.execute(
        "SELECT id, username, email, password FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    connection.close()

    if not user:
        return jsonify({"message": "Invalid username or password"}), 401

    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid username or password"}), 401

    return jsonify(
        {
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"]
            }
        }
    )


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
