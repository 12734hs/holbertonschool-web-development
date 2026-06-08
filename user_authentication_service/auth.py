#!/usr/bin/env python3
"""This file is about auth in our service"""
import bcrypt

def _hash_password(password: str) -> None:
    """method which hashes and convert it to bytes"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')