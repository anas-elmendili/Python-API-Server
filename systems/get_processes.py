from flask import Blueprint, jsonify
from db.auth import token_required
import psutil

processes_bp = Blueprint('processes', __name__, url_prefix='/processes')

@processes_bp.route('/', methods=['GET'])
@token_required
def get_processes():
    try:
        procs = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            procs.append(proc.info)
            if len(procs) >= 50:
                break
        return jsonify(procs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from . import post_processes, delete_processes