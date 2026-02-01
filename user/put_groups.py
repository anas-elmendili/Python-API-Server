from flask import jsonify
from db.auth import token_required, get_request_data
from .get_groups import groups_bp
from utils.command_runner import run_system_command

@groups_bp.route('/<groupname>', methods=['PUT'])
@token_required
def update_group(groupname):
    data = get_request_data()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing new name"}), 400

    new_name = data['name']
    res = run_system_command(["groupmod", "-n", new_name, groupname])
    
    if not res['success']:
        return jsonify({"error": f"Failed to update group: {res['error']}"}), 400
        
    return jsonify({"message": f"Group {groupname} renamed to {new_name}"})