from flask import request, jsonify
from db.auth import token_required, get_request_data
from .get_groups import groups_bp
from utils.command_runner import run_system_command

@groups_bp.route('/', methods=['POST'])
@token_required
def create_group():
    data = get_request_data()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    group_name = data['name']
    res = run_system_command(["groupadd", group_name])
    
    if not res['success']:
        return jsonify({"error": f"Failed to create group: {res['error']}"}), 400
        
    return jsonify({"message": f"Group {group_name} created"}), 201