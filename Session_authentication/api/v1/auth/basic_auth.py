#!/usr/bin/env python3
"""This is documentation for the file"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """This is basic auth documented class baby"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """This is a method we use for takuing the code"""
        if (authorization_header is None or
                type(authorization_header) is not str):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """This is a method which we use for decode the header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            import base64
            decoded_bytes = base64.b64decode(
                base64_authorization_header, validate=True)
            return decoded_bytes.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """This is the method which can explore us the data which
        was included in this special code"""
        a = None
        b = None
        if decoded_base64_authorization_header is None:
            return a, b
        if not isinstance(decoded_base64_authorization_header, str):
            return a, b
        if ':' not in decoded_base64_authorization_header:
            return a, b
        a, b = decoded_base64_authorization_header.split(':')
        return a, b

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """A function that returns the User instance
        based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        from models.user import User
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A function that overloads Auth and
        retrieves the User instance for a request
        """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        base64 = self.extract_base64_authorization_header(auth_header)
        decoded_bytes = self.decode_base64_authorization_header(base64)
        user_name, password = self.extract_user_credentials(decoded_bytes)
        user = self.user_object_from_credentials(user_name, password)
        return user