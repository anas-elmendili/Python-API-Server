from flask import Blueprint, jsonify
import psutil, platform, socket, time
from db.auth import token_required
from functions import *

system_bp = Blueprint("system", __name__, url_prefix="/system")

def safe(callable_):
    try:
        return callable_()
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return None
@system_bp.route("/", methods=["GET"])
@token_required
def all_system_info():
    return jsonify(get_system_info()), 200
