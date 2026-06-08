#!/usr/bin/env python3
"""THis file is the basic file of our project"""
import flask
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def main():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=True)
def users():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({'email': f'{email}', 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'])
def session():
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email=email, password=password):
        return abort(401)

    session_id = AUTH.create_session(email=email)
    response_payload = jsonify({'email': f'{email}', "message": "logged in"})
    response = make_response(response_payload)
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    ss_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(ss_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(ss_id)
    return redirect('/')


@app.route('/profile')
def profile():
    ss_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(ss_id)
    if user is None:
        abort(403)
    return jsonify({'email': f'{user.email}'}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({'email': email, 'reset_token': reset_token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
