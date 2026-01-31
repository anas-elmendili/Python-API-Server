from flask import jsonify
from db.auth import token_required
from db.db_connexion import get_db
from .get_users import users_bp

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    if cur.rowcount == 0:
        return jsonify({"error": "User not found"}), 404
    db.commit()
    return jsonify({"message": "User deleted"})
