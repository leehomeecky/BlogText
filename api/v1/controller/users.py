#!/usr/bin/python3
"""Create a new view for User object that
handles all default RESTFul API actions:"""

from sqlalchemy import *
from sqlalchemy.orm import *
from flask import abort, jsonify, make_response, request
from api.v1.controller.path import app_controller
from models import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
def serialize_user(user):
    """Serialize a User object to a JSON-serializable format."""
    return {
        'UserId': user.userid,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'filepath': user.filepath,
        'created': user.created,
        'email': user.email,
        'password': user.password,
        
        # Add other User attributes here
    }
@app_controller.route('/user/login/', methods=['POST'], strict_slashes = False)
def login():
    """login user in """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    email = request.get_json().get('email')
    pwd = request.get_json().get('password')
    password_ = hashlib.md5(pwd.encode()).hexdigest()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid username or password"}), 401
    if user.password != password_:
        return make_response(jsonify({'error': 'Invalid username or password'}), 401)
    else:
        access_token = create_access_token(identity=user.email)
        return jsonify(access_token=access_token)

@app_controller.route('/users', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
    """Create a new view for User object that handles
    all default RESTFul API actions:"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({"message": "Not a valid user"}), 401
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"message": "Not a valid user"}), 401

    users = User.query.order_by(User.created.desc())
    serialized_users = [serialize_user(user) for user in users]
    return jsonify(serialized_users)

@app_controller.route('/users/<int:id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(id):
    """Create a new view for User object that handles
    all default RESTFul API actions:"""
    # users = []
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    serialized_user = serialize_user(user)
    return jsonify(serialized_user)


@app_controller.route('/users/<int:id>', methods=['DELETE'],
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

@app_controller.route('/users', methods=['POST'], strict_slashes=False)
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

@app_controller.route('/users/<int:id>', methods=['PUT'],
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

