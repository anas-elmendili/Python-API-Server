from flask import Flask
from db.auth import auth_bp
from systems.get_systems import systems_bp, files_bp
from systems.get_processes import processes_bp
from user.get_users import users_bp
from user.get_groups import groups_bp
from db.db_connexion import init_db

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(systems_bp)
app.register_blueprint(files_bp)
app.register_blueprint(processes_bp)
app.register_blueprint(users_bp)
app.register_blueprint(groups_bp)

if __name__ == "__main__":
    # Ensure DB is initialized
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)