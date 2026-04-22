#!/usr/bin/env python3
"""This is document about handlers"""
from unittest import result

from api.v1.views import app_views
from flask import abort, request, jsonify
import os

@app_views.route('/auth_session/login',methods=['POST'], strict_slashes=True)
def session_login():
    """Login function"""
    email = request.form.get('email')
    pswd = request.form.get('password')

    if email is None or email == '':
        return jsonify({'error': 'email missing'}), 400

    if pswd is None or pswd == '':
        return jsonify({'error': 'password missing'}), 400

    from models.user import User

    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({'error': 'no user found for this email'}), 404

    user = users[0]

    if not user.is_valid_password(pswd):
        return jsonify({'error': 'wrong password'}), 401

    from api.v1.app import auth
    session_code = auth.create_session(user.id)
    response = (user.to_json())
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_code)

    return response