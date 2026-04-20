#!/usr/env/bin python
"""This file we use for create auth funct in our app"""
from flask import request
from typing import List, TypeVar

class Auth:
    """We gonna use that class for auth goals"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        return False


    def authorization_header(self, request=None) -> str:
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        return None