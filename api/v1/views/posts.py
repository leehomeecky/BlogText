#!/usr/bin/python3
"""Create a new view for User object that
handles all default RESTFul API actions:"""

from sqlalchemy import *
from sqlalchemy.orm import *
from flask import abort, jsonify, make_response, request
from api.v1.views.path import app_views
from models import *

def serialized_posts(post):
    """Serialize a User object to a JSON-serializable format."""
    return {
        'id': post.id,
        'title': post.title,
        'user_id': post.user_id,
        'filepath': post.filepath,
        'created': post.created,
        'body': post.body,
        'slug': post.slug,

        # Add other User attributes here
    }


@app_views.route('/users/<user_id>/posts', methods=['GET'],
                 strict_slashes=False)
def get_posts_by_userId(user_id):
    """
    Retrieves the list of all posts objects
    of a specific User, or a specific user
    """
    list_cities = []
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)
    for post in user.posts:
        list_cities.append(serialized_posts(post))
    return jsonify(list_cities)

@app_views.route('/posts', methods=['GET'], strict_slashes=False)
def get_posts():
    """Create a new view for post object that handles
    all default RESTFul API actions:"""
    # users = []
    posts = Post.query.order_by(Post.created.desc())
    serialized_post = [serialized_posts(post) for post in posts]
    return jsonify(serialized_post)

@app_views.route('/posts/<int:id>', methods=['GET'], strict_slashes=False)
def get_post_by_id(id):
    """Create a new view for post object that handles
    all default RESTFul API actions:"""
    # users = []
    post = Post.query.filter_by(id=id).first()
    if post is None:
        abort(404)
    serialized_post = serialized_posts(post)
    return jsonify(serialized_post)

@app_views.route('/posts/<int:id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_post(id):
    """Create a new view for User object that
    handles all default RESTFul API actions:"""
    post = Post.query.filter_by(id=id).first()
    if post is None:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return (jsonify({}))

@app_views.route('/users/<user_id>/posts', methods=['POST'], strict_slashes=False)
def post_blog(user_id):
    """Create a new view for User object
    that handles all default RESTFul API actions:"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'title' not in request.get_json():
        return make_response(jsonify({'error': 'Missing title'}), 400)
    if 'body' not in request.get_json():
        return make_response(jsonify({'error': 'Missing body'}), 400)
    post = Post(**request.get_json())
    post.user_id = user.id
    db.session.add(post)
    db.session.commit()
    return make_response(jsonify(serialized_posts(post)), 201)