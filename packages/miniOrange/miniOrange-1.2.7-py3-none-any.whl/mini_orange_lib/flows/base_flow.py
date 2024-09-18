import secrets
from flask import session

class BaseAuthorizationFlow:
    def __init__(self, config):
        self.config = config
        self.state = None

    def generate_state(self):
        self.state = secrets.token_urlsafe(16)
        session['state'] = self.state
        return self.state

    def build_auth_url(self):
        raise NotImplementedError("Subclasses should implement this!")

    def handle_callback_response(self, uri):
        raise NotImplementedError("Subclasses should implement this!")
