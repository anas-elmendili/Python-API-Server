from flask import request, jsonify
from werkzeug.security import generate_password_hash
from db.auth import token_required, get_request_data
from db.db_connexion import get_db
from .get_users import users_bp

@users_bp.route('/', methods=['POST'])
@token_required
def create_user():
    data = get_request_data()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing data"}), 400

    db = get_db()
    cur = db.cursor()
    hashed = generate_password_hash(data['password'])
    try:
        cur.execute("INSERT INTO users (username, password, group_id) VALUES (?, ?, ?)",
                    (data['username'], hashed, data.get('group_id')))
        db.commit()
        return jsonify({"message": "User created"}), 201
    except Exception:
        return jsonify({"error": "User exists"}), 409