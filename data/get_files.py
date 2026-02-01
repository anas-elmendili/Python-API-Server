import os
import pwd
import grp
import stat
import time
from flask import Blueprint, jsonify, request
from db.auth import token_required, get_request_data
from .post_files import create_item
from .put_files import update_item
from .delete_files import delete_item

files_bp = Blueprint('files', __name__, url_prefix='/files')

def is_safe_path(path):
    if not path: return False
    # Allow absolute paths, just block traversal up
    return ".." not in path

def list_files(directory="."):
    """Lists files and directories with detailed metadata (ls -la style)."""
    try:
        items = []
        # Use scandir for better performance and easier type checking
        with os.scandir(directory) as it:
            for entry in it:
                try:
                    s = entry.stat()
                    
                    # Get Owner and Group names
                    try:
                        uid = s.st_uid
                        gid = s.st_gid
                        owner = pwd.getpwuid(uid).pw_name
                        group = grp.getgrgid(gid).gr_name
                    except KeyError:
                        owner = str(uid)
                        group = str(gid)
                    
                    # File Type
                    if entry.is_dir():
                        ftype = "directory"
                    elif entry.is_file():
                        ftype = "file"
                    elif entry.is_symlink():
                        ftype = "symlink"
                    else:
                        ftype = "other"
                        
                    items.append({
                        "name": entry.name,
                        "type": ftype,
                        "owner": owner,
                        "permissions": stat.filemode(s.st_mode),
                        "group": group,
                        "size": s.st_size,
                        "modified": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(s.st_mtime))
                    })
                except OSError:
                    # Skip files we can't access
                    continue
                    
        return {"files": items}
    except Exception as e:
        return {"error": str(e)}

def read_file_content(path):
    """Reads content of a file."""
    try:
        if not os.path.exists(path):
            return {"error": "File not found"}
        with open(path, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

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
        err = result['error'].lower()
        if "not found" in err or "no such file" in err or "does not exist" in err:
             return jsonify(result), 404
        return jsonify(result), 500
    return jsonify(result)

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

@files_bp.route('/', methods=['PUT'])
@token_required
def update_file_route():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Missing path parameter"}), 400

    data = get_request_data()
    if not data:
         return jsonify({"error": "No data provided"}), 400
    
    if not is_safe_path(path):
         return jsonify({"error": "Invalid path"}), 400

    content = data.get('content')
    permissions = data.get('chmod')
    owner = data.get('chown')

    result = update_item(path, content, permissions, owner)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

@files_bp.route('/', methods=['DELETE'])
@token_required
def delete_file_route():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Missing path parameter"}), 400
        
    if not is_safe_path(path):
         return jsonify({"error": "Invalid path"}), 400
         
    recursive = request.args.get('recursive', 'false').lower() == 'true'

    result = delete_item(path, recursive)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result)