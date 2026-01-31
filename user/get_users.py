from flask import Blueprint, jsonify
from db.auth import token_required
from db.db_connexion import get_db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
@token_required
def list_users():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, username, group_id FROM users")
    rows = cur.fetchall()
    users = [dict(row) for row in rows]
    return jsonify(users)

from . import post_users, put_users, delete_users