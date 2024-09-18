from .base_flow import BaseAuthorizationFlow
from mini_orange_lib.token_service import AuthorizationTokenHandler

class AuthorizationCodeFlow(BaseAuthorizationFlow):
    def build_auth_url(self) -> str:
        base_url = self.config.base_url
        client_id = self.config.credentials.client_id
        redirect_url = self.config.redirect_url
        state = self.generate_state()

        auth_url = (
            f"{base_url}/moas/idp/openidsso?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_url}&"
            f"scope=openid&"
            f"response_type=code&"
            f"state={state}"
        )
        return auth_url

    def handle_callback_response(self, uri):
        return AuthorizationTokenHandler(self.config).handle_callback_response(uri)
