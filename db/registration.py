from flask import Blueprint, request, jsonify
from .db_connexion import get_db
import secrets

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/registration", methods=["POST"])
def registration():
    name = request.args.get("name")
    email = request.args.get("email")

    if not name or not email:
        return {"error": "Both 'name' and 'email' are required"}, 400

    token = secrets.token_hex(16)

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO users (name, email, token) VALUES (?, ?, ?)",
                    (name, email, token))
        db.commit()
    except Exception:
        db.close()
        return {"error": "Email already registered"}, 400

    db.close()
    return {"message": "User registered successfully", "token": token}, 201
