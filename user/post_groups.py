from flask import request, jsonify
from db.auth import token_required, get_request_data
from db.db_connexion import get_db
from .get_groups import groups_bp

@groups_bp.route('/', methods=['POST'])
@token_required
def create_group():
    data = get_request_data()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO groups (name) VALUES (?)", (data['name'],))
        db.commit()
        return jsonify({"message": "Group created"}), 201
    except Exception:
        return jsonify({"error": "Group exists"}), 409