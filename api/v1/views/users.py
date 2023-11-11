#!/usr/bin/python3
"""Create a new view for User object that
handles all default RESTFul API actions:"""

from sqlalchemy import *
from sqlalchemy.orm import *
from flask import abort, jsonify, make_response, request
from api.v1.views.path import app_views
from models import *
def serialize_user(user):
    """Serialize a User object to a JSON-serializable format."""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'filepath': user.filepath,
        'created': user.created,
        'email': user.email,
        'password': user.password,
        
        # Add other User attributes here
    }
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Create a new view for User object that handles
    all default RESTFul API actions:"""
    # users = []
    users = User.query.all()
    serialized_users = [serialize_user(user) for user in users]
    return jsonify(serialized_users)

@app_views.route('/users/<int:id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(id):
    """Create a new view for User object that handles
    all default RESTFul API actions:"""
    # users = []
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    serialized_user = serialize_user(user)
    return jsonify(serialized_user)


@app_views.route('/users/<int:id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(id):
    """Create a new view for User object that
    handles all default RESTFul API actions:"""
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return (jsonify({}))

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a new view for User object
    that handles all default RESTFul API actions:"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    if 'first_name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing first name'}), 400)
    if 'last_name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing last name'}), 400)
    user = User(**request.get_json())
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify(serialize_user(user)), 201)

@app_views.route('/users/<int:id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(id):
    """Create a new view for User object that
    handles all default RESTFul API actions:"""
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'email', 'created']:
            setattr(user, attr, val)
    db.session.commit()
    return jsonify(serialize_user(user))

