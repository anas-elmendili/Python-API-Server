from flask import request, jsonify
from db.auth import token_required, get_request_data
from db.db_connexion import get_db
from .get_groups import groups_bp

@groups_bp.route('/<int:group_id>', methods=['PUT'])
@token_required
def update_group(group_id):
    data = get_request_data()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("UPDATE groups SET name = ? WHERE id = ?", (data['name'], group_id))
        if cur.rowcount == 0:
            return jsonify({"error": "Group not found"}), 404
        db.commit()
        return jsonify({"message": "Group updated"})
    except Exception:
        return jsonify({"error": "Name conflict"}), 409