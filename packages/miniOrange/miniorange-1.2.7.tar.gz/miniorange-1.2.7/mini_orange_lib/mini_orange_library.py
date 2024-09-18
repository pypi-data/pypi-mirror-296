import logging
from mini_orange_lib import AuthorizationTokenHandler, Config
from mini_orange_lib.flows import AuthorizationCodeFlow, PKCEAuthorizationFlow, ImplicitAuthorizationFlow,OAuthPasswordFlowManager

class MiniOrangeLibrary:
    def __init__(self, config: Config):
        if not isinstance(config, Config):
            raise TypeError("Expected config to be an instance of Config")

        self.config = config

        # Initialize the token handler and password flow manager
        self.token_response_handler = AuthorizationTokenHandler(config)
        self.password_flow = OAuthPasswordFlowManager(config)

        # Initialize different authorization flows
        self.auth_flows = {
            'auth_code': AuthorizationCodeFlow(config),
            'auth_pkce': PKCEAuthorizationFlow(config),
            'implicit': ImplicitAuthorizationFlow(config),
        }

    def start_authentication(self, grant_type: str) -> str:
        if grant_type not in self.auth_flows:
            raise ValueError(f"Unsupported grant type: {grant_type}")
        auth_flow = self.auth_flows[grant_type]
        return auth_flow.build_auth_url()

    def handle_callback_response(self, uri: str, code_verifier: str = None) -> dict:
        try:
            # Process the callback response and extract user information
            user_info = self.token_response_handler.handle_callback_response(uri, code_verifier)
            return user_info
        except Exception as e:
            logging.error(f"Error handling authentication response: {e}")
            return {"status": "failure", "message": str(e)}

    def handle_password_grant_flow(self, username: str, password: str) -> dict:
        try:
            # Request access token and retrieve user information
            user_info = self.password_flow.handle_password_grant_flow(username, password)
            return user_info
        except Exception as e:
            logging.error(f"Error requesting token with password: {e}")
            return {"status": "failure", "message": str(e)}
