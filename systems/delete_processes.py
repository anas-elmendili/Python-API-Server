from flask import jsonify, request
from db.auth import token_required
from .get_processes import processes_bp
import psutil

@processes_bp.route('/<int:pid>', methods=['DELETE'])
@token_required
def delete_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return jsonify({"message": f"Process {pid} terminated"})
    except psutil.NoSuchProcess:
        return jsonify({"error": "Process not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
