from flask import Blueprint, jsonify, request
from db.auth import token_required
import platform
import psutil

systems_bp = Blueprint('systems', __name__, url_prefix='/systems')

# --- System Routes ---
@systems_bp.route('/', methods=['GET'])
@token_required
def get_system_info():
    try:
        info = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "memory": psutil.virtual_memory()._asdict()
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ensure sub-modules are loaded
from . import post_systems, delete_systems