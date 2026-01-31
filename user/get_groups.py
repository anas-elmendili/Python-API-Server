from flask import Blueprint, jsonify
from db.auth import token_required
from db.db_connexion import get_db

groups_bp = Blueprint('groups', __name__, url_prefix='/groups')

@groups_bp.route('/', methods=['GET'])
@token_required
def list_groups():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM groups")
    rows = cur.fetchall()
    groups = [dict(row) for row in rows]
    return jsonify(groups)

from . import post_groups, put_groups