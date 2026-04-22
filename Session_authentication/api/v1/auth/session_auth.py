#!/usr/bin/env python3
"""It is a documentation for this file"""
from api.v1.auth.auth import Auth
from uuid import uuid4

class SessionAuth(Auth):
    """This class is about session mechanism in flask"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """We use that method for summon the session for user"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_code = uuid4()
        self.user_id_by_session_id[str(session_code)] = user_id
        return str(session_code)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """We us ethis method for find user by his session"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """We use this method for get a user instance"""
        from models.user import User
        coks = self.session_cookie(request)
        id = self.user_id_by_session_id[coks]
        return User.get(id)