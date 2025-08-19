from flask import Blueprint, request, jsonify
from services.hash import check_password, hash_password
from models.db import get_hashed_pass, set_hashed_pass
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return 'bad request', 400

    pwd_hash = get_hashed_pass(username)

    if not pwd_hash:
        return 'incorrect username or password', 401

    if check_password(pwd_hash, password):
        access_token = create_access_token(identity=username)
        response = jsonify({"msg": "Login successful"})
        set_access_cookies(response, access_token)
        return response
    else:
        return 'incorrect username or password', 401

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    pwd_hash = hash_password(password)

    if set_hashed_pass(username, pwd_hash):
        access_token = create_access_token(identity=username)
        response = jsonify({"msg": "Register successful"})
        set_access_cookies(response, access_token)
        return response
    else:
        return 'error', 401


