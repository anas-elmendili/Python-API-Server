from flask import request, jsonify
from werkzeug.security import generate_password_hash
import secrets

from .db_connexion import get_db
from .auth import auth_bp, get_request_data


@auth_bp.route("/register", methods=["POST"])
def register():
    data = get_request_data()
    if not data:
        return jsonify({"error": "Request must be JSON"}), 415

    username = data.get("username")
    password = data.get("password")
    group_id = data.get("group_id")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    hashed_password = generate_password_hash(password)
    token = secrets.token_hex(16)

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (username, password, group_id, token)
            VALUES (?, ?, ?, ?)
            """,
            (username, hashed_password, group_id, token)
        )
        db.commit()
    except Exception:
        db.close()
        return jsonify({"error": "User already exists"}), 409

    db.close()

    return jsonify({
        "message": "User registered successfully",
        "token": token
    }), 201

