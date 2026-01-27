from functools import wraps
from flask import request, jsonify
from .db_connexion import get_db
import secrets

def log_request(token):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO logs (token, method, endpoint, ip) VALUES (?, ?, ?, ?)",
        (token, request.method, request.path, request.remote_addr)
    )
    db.commit()
    db.close()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM users WHERE token = ?", (token,))
        user = cur.fetchone()
        db.close()

        if not user:
            return jsonify({"error": "Invalid token"}), 403

        log_request(token)
        return f(*args, **kwargs)
    return decorated
