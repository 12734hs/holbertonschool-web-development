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
        self.user_id_by_session_id[session_code] = user_id
        return session_code
