from flask import request, jsonify
from werkzeug.security import generate_password_hash
from db.auth import token_required, get_request_data
from db.db_connexion import get_db
from .get_users import users_bp

@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    data = get_request_data()
    db = get_db()
    cur = db.cursor()
    
    fields = []
    values = []
    
    if 'password' in data:
        fields.append("password = ?")
        values.append(generate_password_hash(data['password']))
    
    if 'group_id' in data:
        fields.append("group_id = ?")
        values.append(data['group_id'])
        
    if not fields:
        return jsonify({"error": "No data to update"}), 400
        
    values.append(user_id)
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
    
    cur.execute(query, values)
    if cur.rowcount == 0:
        return jsonify({"error": "User not found"}), 404
        
    db.commit()
    return jsonify({"message": "User updated"})