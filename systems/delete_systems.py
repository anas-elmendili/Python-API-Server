from flask import jsonify
from db.auth import token_required
from .get_systems import systems_bp

@systems_bp.route('/', methods=['DELETE'])
@token_required
def delete_system_resource():
    # Placeholder
    return jsonify({"error": "Cannot delete system"}), 403
