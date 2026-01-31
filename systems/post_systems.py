from flask import jsonify, request
from db.auth import token_required, get_request_data
from .get_systems import systems_bp

@systems_bp.route('/', methods=['POST'])
@token_required
def post_system_action():
    data = get_request_data()
    # Logic for system action based on data
    return jsonify({"message": "System action received", "data": data}), 200