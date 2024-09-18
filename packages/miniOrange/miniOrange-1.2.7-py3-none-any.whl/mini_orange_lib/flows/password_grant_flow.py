from typing import Dict
import requests
from urllib.parse import urlencode
import logging
from mini_orange_lib.exceptions import TokenRequestError , AuthorizationError
from mini_orange_lib.config import Config

# Manages OAuth Password Grant flow for authentication and user information retrieval.
class OAuthPasswordFlowManager:
    def __init__(self , config: Config):
        if not isinstance( config , Config ):
            raise TypeError( "Expected config to be an instance of Config" )
        self.config = config

    # Requests an access token using username and password.
    def get_token_with_password_grant(self , username: str , password: str) -> Dict:

        # Retrieve base URL and credentials from the config
        base_url = self.config.base_url
        client_id = self.config.credentials.client_id
        client_secret = self.config.credentials.client_secret

        # Validate that both username and password are provided
        if not username or not password:
            raise ValueError( "Username and password must be provided" )

        # Construct the parameters for the token request
        params = {
            'grant_type': 'password' ,
            'client_id': client_id ,
            'client_secret': client_secret ,
            'username': username ,
            'password': password
        }
        post_url = f"{base_url}/moas/rest/oauth/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            # Send POST request to obtain the access token
            response = requests.post( post_url , data=urlencode( params ) , headers=headers )

            # Raises an HTTPError for bad responses
            response.raise_for_status()

            # Token response store in data
            data = response.json()
            logging.debug( f"Token endpoint response: {data}" )
            return data

        except requests.RequestException as e:
            logging.error( f"Request error: {str( e )}" )
            raise TokenRequestError( f"Token request failed: {str( e )}" )

    # Retrieves user information using the provided access token.
    def retrieve_user_info(self , access_token: str) -> dict:

        # Ensure that the access token is provided
        if not access_token:
            raise ValueError( "Access token must be provided" )

        # Prepare the URL and headers for the user info request
        user_info_url = f"{self.config.base_url}/moas/rest/oauth/getuserinfo"
        headers = {
            'Authorization': f'Bearer {access_token}' ,
            'Content-Type': 'application/json'
        }

        try:
            logging.debug( f"Sending request to {user_info_url} with headers: {headers}" )

            # Send GET request to fetch user information
            response = requests.get( user_info_url , headers=headers )

            # Raises an HTTPError for bad responses
            response.raise_for_status()

            # UserInfo response store in user_info
            user_info = response.json()
            logging.debug( f"User info response: {user_info}" )
            return user_info

        except requests.HTTPError as http_err:
            logging.error( f"HTTP error occurred: {http_err}" )
            raise AuthorizationError( f"HTTP error occurred: {http_err}" )

        except requests.RequestException as req_err:
            logging.error( f"Request error: {req_err}" )
            raise AuthorizationError( f"Request error: {req_err}" )

        except ValueError as json_err:
            logging.error( f"Error parsing JSON response: {json_err}" )
            raise AuthorizationError( f"Error parsing JSON response: {json_err}" )

        except Exception as e:
            logging.error( f"Unexpected error: {e}" )
            raise AuthorizationError( f"Unexpected error: {e}" )

    # Authenticates the user with the password grant flow and retrieves their information.
    def handle_password_grant_flow(self , username: str , password: str) -> dict:
        try:

            # Get access token using password grant
            token_response = self.get_token_with_password_grant( username , password )
            access_token = token_response.get( 'access_token' )

            # Ensure that the access token is present in the response
            if not access_token:
                raise ValueError( "Access token not found in the response" )

            # Retrieve user information using the access token
            user_info = self.retrieve_user_info( access_token )
            return user_info

        except Exception as e:
            logging.error( f"Authentication and user info fetch failed: {str( e )}" )
            raise e
