from flask import Blueprint, request, jsonify, render_template
from models.db import get_posts_from_db

posts_bp = Blueprint("posts", __name__)

@posts_bp.route('/get_posts', methods=['GET'])
def get_posts():
    data = get_posts_from_db()
    if not data:
        return jsonify({"msg": "Failed to get posts"}), 500
    
    posts = []
    for post in data:
        post_id, author, text, image, likes = post
        posts.append({
            "id": post_id,
            "author": author,
            "text": text,
            "image": image if image else None, 
            "likes": likes if likes else 0
        })
    
    return jsonify({"posts": posts}), 200
    
    