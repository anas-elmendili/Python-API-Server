from flask import jsonify, request
from db.auth import token_required, get_request_data
from .get_processes import processes_bp
import subprocess

@processes_bp.route('/', methods=['POST'])
@token_required
def create_process():
    data = get_request_data()
    if not data or 'command' not in data:
        return jsonify({"error": "Missing command"}), 400
    
    command = data['command']
    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({"message": "Process started", "pid": proc.pid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500