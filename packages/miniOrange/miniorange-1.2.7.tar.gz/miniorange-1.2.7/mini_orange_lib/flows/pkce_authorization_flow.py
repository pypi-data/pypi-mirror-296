from flask import session

from .base_flow import BaseAuthorizationFlow
from mini_orange_lib.utils.pkce_utils import generate_pkce_pair
from mini_orange_lib.token_service import AuthorizationTokenHandler

class PKCEAuthorizationFlow(BaseAuthorizationFlow):
    def build_auth_url(self):
        code_verifier, code_challenge = generate_pkce_pair()
        session['code_verifier'] = code_verifier
        state = self.generate_state()
        base_url = self.config.base_url
        redirect_url = self.config.redirect_url
        client_id = self.config.credentials.client_id

        auth_url = (
            f"{base_url}/moas/idp/openidsso?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_url}&"
            f"scope=openid&"
            f"response_type=code&"
            f"state={state}&"
            f"code_challenge={code_challenge}&"
            f"code_challenge_method=S256"
        )
        return auth_url

    def handle_callback_response(self, uri):
        code_verifier = session.get('code_verifier')
        return AuthorizationTokenHandler(self.config).handle_callback_response(uri, code_verifier)
