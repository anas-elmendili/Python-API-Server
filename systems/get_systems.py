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
    return ".." not in path and not path.startswith("/")

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
    if not is_safe_path(path) and path != ".":
         return jsonify({"error": "Invalid path"}), 400
    
    result = list_files(path)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@files_bp.route('/<path:filename>', methods=['GET'])
@token_required
def get_file_content_route(filename):
    if not is_safe_path(filename):
         return jsonify({"error": "Invalid path"}), 400
    
    result = read_file_content(filename)
    if "error" in result:
        status = 404 if result['error'] == "File not found" else 500
        return jsonify(result), status
    return jsonify(result)

# Logic for other methods
from data.post_files import create_file
from data.put_files import update_file
from data.delete_files import delete_file_data

@files_bp.route('/', methods=['POST'])
@token_required
def create_file_route():
    data = get_request_data()
    if not data or 'path' not in data:
        return jsonify({"error": "Missing path"}), 400
    
    path = data['path']
    content = data.get('content', '')
    if not is_safe_path(path):
         return jsonify({"error": "Invalid path"}), 400

    result = create_file(path, content)
    if "error" in result:
        return jsonify(result), 409
    return jsonify(result), 201

@files_bp.route('/<path:filename>', methods=['PUT'])
@token_required
def update_file_route(filename):
    data = get_request_data()
    if not data or 'content' not in data:
        return jsonify({"error": "Missing content"}), 400
    
    if not is_safe_path(filename):
         return jsonify({"error": "Invalid path"}), 400

    result = update_file(filename, data['content'])
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result)

@files_bp.route('/<path:filename>', methods=['DELETE'])
@token_required
def delete_file_route(filename):
    if not is_safe_path(filename):
         return jsonify({"error": "Invalid path"}), 400

    result = delete_file_data(filename)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result)

# Ensure sub-modules are loaded
from . import post_systems, delete_systems