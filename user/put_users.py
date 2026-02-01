from flask import jsonify
from db.auth import token_required, get_request_data
from .get_users import users_bp
from utils.command_runner import run_system_command

@users_bp.route('/<username>', methods=['PUT'])
@token_required
def update_user(username):
    data = get_request_data()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'password' in data:
        res = run_system_command(["chpasswd"], input_text=f"{username}:{data['password']}")
        if not res['success']:
             return jsonify({"error": f"Failed to update password: {res['error']}"}), 400

    commands = []
    if 'groups' in data:
        # data['groups'] should be "sudo,docker"
        commands.extend(["-aG", data['groups']])
    
    if 'shell' in data:
        commands.extend(["-s", data['shell']])

    if commands:
        full_command = ["usermod"] + commands + [username]
        res = run_system_command(full_command)
        if not res['success']:
            return jsonify({"error": f"Failed to update user: {res['error']}"}), 400

    return jsonify({"message": f"User {username} updated"})