#!/usr/bin/env python3
"""This file is about auth in our service"""
import uuid
from uuid import UUID

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """method which hashes and convert it to bytes"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """We use that method for creating user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hash_pwd = _hash_password(password)
            return self._db.add_user(email, hash_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Create method for valid login"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password.encode('utf-8')):
                return True
        except (NoResultFound, AttributeError):
            return False
        return False

    def create_session(self, email: str) -> str:
        """This method created a new session id"""
        user = self._db.find_user_by(email=email)
        if not user:
            raise NoResultFound
        else:
            ss_id = _generate_uuid()
            self._db.update_user(user.id, session_id=ss_id)
            return str(ss_id)

    def get_user_from_session_id(self, session_id: str) -> User:
        """This method helps us find user by his ss id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if not user:
                return None
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id):
        """This method destroys session id"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email):
        """We use that method for get and provide reset token to user"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token, password):
        """This method we use for change password in profile"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        new_psw = _hash_password(password)
        self._db.update_user(user.id, hashed_password=new_psw,
                             reset_token=None)

        return None
