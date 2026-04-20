#!/usr/bin/env python3
"""This is documentation for the file"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """This is basic auth documented class baby"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """We will use this method for taking basic from the header"""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        lst = authorization_header.split(' ')
        if lst[0] is not 'Basic':
            return None
        return lst[1]
