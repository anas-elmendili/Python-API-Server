from flask import request, jsonify
from db.auth import token_required, get_request_data
from .get_users import users_bp
from utils.command_runner import run_system_command

@users_bp.route('/', methods=['POST'])
@token_required
def create_user():
    data = get_request_data()
    if not data or 'username' not in data:
        return jsonify({"error": "Missing username"}), 400

    username = data['username']
    password = data.get('password')
    
    # Create user
    res = run_system_command(["useradd", "-m", "-s", "/bin/bash", username])
    if not res['success']:
        return jsonify({"error": f"Failed to create user: {res['error']}"}), 400
        
    if password:
        # Set password
        pass_res = run_system_command(["chpasswd"], input_text=f"{username}:{password}")
        if not pass_res['success']:
             return jsonify({"error": f"User created but failed to set password: {pass_res['error']}"}), 400
            
    return jsonify({"message": f"User {username} created successfully"}), 201