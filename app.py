from flask import Flask
from db.routes import auth_bp
from system.all import system_bp
from processes.routes import process_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(system_bp)
app.register_blueprint(process_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
