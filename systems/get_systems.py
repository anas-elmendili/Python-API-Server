from flask import Blueprint, jsonify, request
from db.auth import token_required, get_request_data
import platform
import psutil
import os
from data.get_files import list_files, read_file_content

systems_bp = Blueprint('systems', __name__, url_prefix='/systems')
files_bp = Blueprint('files', __name__, url_prefix='/files')

def is_safe_path(path):
    if not path: return False
    # Allow absolute paths, just block traversal up
    return ".." not in path

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

# --- File Routes ---
@files_bp.route('/', methods=['GET'])
@token_required
def get_files_route():
    path = request.args.get('path', '.')
    if not is_safe_path(path):
         return jsonify({"error": "Invalid path"}), 400
    
    if os.path.isfile(path):
        result = read_file_content(path)
    else:
        result = list_files(path)
        
    if "error" in result:
        return jsonify(result), 404 if "not found" in result['error'].lower() else 500
    return jsonify(result)

# Logic for other methods
from data.post_files import create_item
from data.put_files import update_item
from data.delete_files import delete_item

@files_bp.route('/', methods=['POST'])
@token_required
def create_file_route():
    data = get_request_data()
    if not data or 'path' not in data:
        return jsonify({"error": "Missing path"}), 400
    
    path = data['path']
    is_dir = data.get('is_dir', False)
    content = data.get('content', '')
    
    if not is_safe_path(path):
         return jsonify({"error": "Invalid path"}), 400

    result = create_item(path, is_dir, content)
    if "error" in result:
        return jsonify(result), 409
    return jsonify(result), 201

@files_bp.route('/<path:filename>', methods=['PUT'])
@token_required
def update_file_route(filename):
    data = get_request_data()
    if not data:
         return jsonify({"error": "No data provided"}), 400
    
    filename = "/" + filename if not filename.startswith("/") else filename
    if not is_safe_path(filename):
         return jsonify({"error": "Invalid path"}), 400

    content = data.get('content')
    permissions = data.get('chmod')
    owner = data.get('chown')

    result = update_item(filename, content, permissions, owner)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

@files_bp.route('/<path:filename>', methods=['DELETE'])
@token_required
def delete_file_route(filename):
    filename = "/" + filename if not filename.startswith("/") else filename
    if not is_safe_path(filename):
         return jsonify({"error": "Invalid path"}), 400
         
    recursive = request.args.get('recursive', 'false').lower() == 'true'

    result = delete_item(filename, recursive)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result)

# Ensure sub-modules are loaded
from . import post_systems, delete_systems