from flask import Flask, render_template
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from models.db import init_db
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.posts import posts_bp
from services.hash import generate_password_hash
import config
import json

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = config.jwt_secret
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(posts_bp)

jwt = JWTManager(app)

@app.route('/', methods=["GET"])
def start():
    verify_jwt_in_request(optional=True)
    username = get_jwt_identity()
    if username == getattr(config, 'admin_username', None):
        return render_template('admin.html')
    return render_template('index.html')

if __name__ == '__main__':
    init_db(generate_password_hash(config.admin_password))
    app.run(host='0.0.0.0', port=9001, threaded=True)
    
    