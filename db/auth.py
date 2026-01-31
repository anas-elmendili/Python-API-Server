from functools import wraps
from flask import Blueprint, request, jsonify
from .db_connexion import get_db
import secrets
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_request_data():
    """Helper to get data from JSON or Form."""
    return request.get_json(silent=True) or request.form.to_dict()

def log_request(token):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO logs (token, method, endpoint, ip) VALUES (?, ?, ?, ?)",
            (token, request.method, request.path, request.remote_addr)
        )
        db.commit()
    except Exception:
        pass

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
        
        if not user:
            return jsonify({"error": "Invalid token"}), 403

        log_request(token)
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    data = get_request_data()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data['username']
    password = data['password']

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()

    if user and check_password_hash(user['password'], password):
        token = secrets.token_hex(16)
        cur.execute("UPDATE users SET token = ? WHERE id = ?", (token, user['id']))
        db.commit()
        return jsonify({"token": token, "user_id": user['id']})
    
    return jsonify({"error": "Invalid credentials"}), 401

# Import registration at the end to avoid circular issues
from . import registration
