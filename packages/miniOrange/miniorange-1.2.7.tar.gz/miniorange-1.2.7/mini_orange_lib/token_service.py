import requests
import logging
from urllib.parse import urlencode, urlparse, parse_qs
from flask import session
from mini_orange_lib.jwt_manager import JWTDecoder
from mini_orange_lib.config import Config
from mini_orange_lib.exceptions import TokenRequestError, InvalidConfigurationError, AuthorizationError


class AuthorizationTokenHandler:
    def __init__(self, config: Config):
        if not isinstance(config, Config):
            raise TypeError("Expected config to be an instance of Config")
        self.config = config
        # Initialize the JWTManager with public key and client ID
        self.jwt_decode = JWTDecoder(config.public_key, config.credentials.client_id)

    # Handles the callback response based on the grant type.
    def handle_callback_response(self, uri: str, code_verifier: str = None) -> dict:

        if not all([self.config.credentials.client_id, self.config.base_url, self.config.redirect_url]):
            raise InvalidConfigurationError(
                parameter_name='client_id/client_secret/redirect_url',
                message="Client ID, Client Secret, or Redirect URL is not set"
            )

        # Parse the URI to handle query and fragment parts
        parsed_uri = urlparse(uri)
        logging.debug(f"Parsed URI: {parsed_uri}")

        if parsed_uri.path == "/callback":

            # Extract query parameters from the URI
            query_params = parse_qs(parsed_uri.query)
            code = query_params.get("code", [None])[0]
            state = query_params.get("state", [None])[0]
            id_token = query_params.get("id_token", [None])[0]
            logging.debug(f"Authorization code: {code}, State: {state}")

            # Verify the state matches the one stored in the session
            if state != session.get('state'):
                logging.debug(f"State:{state},State_Session:{self.state}")
                raise AuthorizationError(message="State is not matching")

            # Handle the authorization code or ID token
            if code:
                return self._exchange_code_for_token(code, code_verifier)
            if id_token:
                user_info = self.jwt_decode.decode_jwt(id_token)
                return user_info
        else:
            raise AuthorizationError(message="Invalid callback URL")

    # Exchanges authorization code for token
    def _exchange_code_for_token(self, code: str, code_verifier: str = None) -> dict:
        code_verifier = session.get('code_verifier')
        logging.debug(f"Requesting token with code: {code} and code_verifier: {code_verifier}")

        # Prepare the parameters for the token request
        base_url = self.config.base_url
        redirect_url = self.config.redirect_url
        client_id = self.config.credentials.client_id
        client_secret = self.config.credentials.client_secret

        params = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_url
        }

        # Include the code verifier if provided (for PKCE flow)
        if code_verifier:
            params['code_verifier'] = code_verifier

        # Define the URL for the OAuth token endpoint
        oauth_token_url = f"{base_url}/moas/rest/oauth/token"

        # Set the headers for the POST request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            logging.debug(f"Sending POST request to URL: {oauth_token_url} with params: {params}")

            # Send the POST request to exchange the authorization code for tokens
            response = requests.post(oauth_token_url, data=urlencode(params), headers=headers)

            response.raise_for_status()
            try:
                # JSON response from the token endpoint
                res = response.json()

                logging.debug(f"Token endpoint response: {res}")

                # Extract the ID token from the response
                id_token = res.get('id_token')

                if id_token:
                    # Decode the ID token to get user information
                    user_info = self.jwt_decode.decode_jwt(id_token)
                    return user_info

            except ValueError:
                logging.error("Failed to decode JSON response")
                raise TokenRequestError("Invalid JSON response from token endpoint")

        except requests.RequestException as e:
            logging.error(f"Request error: {str(e)}")
            raise TokenRequestError(f"Token request failed: {str(e)}")
