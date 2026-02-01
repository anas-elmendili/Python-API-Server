from flask import Blueprint, jsonify
from db.auth import token_required
import grp

groups_bp = Blueprint('groups', __name__, url_prefix='/groups')

@groups_bp.route('/', methods=['GET'])
@token_required
def list_groups():
    try:
        groups = []
        for g in grp.getgrall():
            groups.append({
                "groupname": g.gr_name,
                "gid": g.gr_gid,
                "members": g.gr_mem
            })
        return jsonify(groups)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from . import post_groups, put_groups