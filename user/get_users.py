from flask import Blueprint, jsonify
from db.auth import token_required
import pwd

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
@token_required
def list_users():
    try:
        users = []
        for p in pwd.getpwall():
            users.append({
                "username": p.pw_name,
                "uid": p.pw_uid,
                "gid": p.pw_gid,
                "gecos": p.pw_gecos,
                "home": p.pw_dir,
                "shell": p.pw_shell
            })
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from . import post_users, put_users, delete_users