from flask import jsonify
from db.auth import token_required
from .get_users import users_bp
from utils.command_runner import run_system_command

@users_bp.route('/<username>', methods=['DELETE'])
@token_required
def delete_user(username):
    res = run_system_command(["userdel", "-r", username])
    if not res['success']:
        return jsonify({"error": f"Failed to delete user: {res['error']}"}), 400
        
    return jsonify({"message": f"User {username} deleted"})
