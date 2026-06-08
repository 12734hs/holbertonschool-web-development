#!/usr/bin/env python3
"""THis file is the basic file of our project"""
import flask
from flask import Flask, jsonify, request, make_response
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def main():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
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
    email = request.get.form('email')
    password = request.get.form('password')
    if not AUTH.valid_login(email=email, password=password):
        return flask.abort(401)

    session_id = AUTH.create_session(email=email)
    response_payload = jsonify({'email': f'{email}', "message": "logged in"})
    response = make_response(response_payload)
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
