from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies
from config import admin_username


admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
@jwt_required()
def admin():
    username = get_jwt_identity()
    if username == admin_username:
        return render_template('admin.html')
    else:
        response = jsonify({"msg": "Access Denied"})
        return response, 403