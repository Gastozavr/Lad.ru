from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies
from config import admin_username
from models.db import save_post_in_db
from werkzeug.utils import secure_filename
import uuid
import os


admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
@jwt_required()
def admin():
    username = get_jwt_identity()
    if username != admin_username:
        response = jsonify({"msg": "Access Denied"})
        return response, 403
        
    return render_template('admin.html')

@admin_bp.route('/create_post', methods=['POST'])
@jwt_required()
def create_post():
    username = get_jwt_identity()
    if username != admin_username:
        response = jsonify({"msg": "Access Denied"})
        return response, 403
    
    text = request.form.get('text')
    image_file = request.files.get('image')
    
    if not text:
        return jsonify({"msg": "Text is required"}), 400
    
    image_filename = None
    if image_file and image_file.filename:
        
        file_ext = os.path.splitext(image_file.filename)[1]
        image_filename = f"post_{uuid.uuid4().hex[:8]}{file_ext}"
        
        static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')
        image_path = os.path.join(static_folder, image_filename)
        image_file.save(image_path)
    
    if save_post_in_db(username, text, image_filename or 'default.jpg'):
        return jsonify({"msg": "Post created successfully"}), 201
    else:
        return jsonify({"msg": "Failed to create post"}), 500
        