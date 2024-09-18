from .base_flow import BaseAuthorizationFlow

class ImplicitAuthorizationFlow(BaseAuthorizationFlow):
    def build_auth_url(self):
        state = self.generate_state()
        base_url = self.config.base_url
        redirect_url = self.config.redirect_url
        client_id = self.config.credentials.client_id

        auth_url = (
            f"{base_url}/moas/idp/openidsso?"
            f"response_type=token&"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_url}&"
            f"scope=openid&"
            f"state={state}"
        )
        return auth_url

    def handle_callback_response(self, uri):
        raise NotImplementedError("Implicit flow response handling is typically done client-side")
