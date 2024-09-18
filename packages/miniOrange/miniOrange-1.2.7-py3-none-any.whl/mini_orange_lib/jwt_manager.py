import logging
from jwt import decode
from mini_orange_lib.exceptions import JwtExpiredSignatureError, JwtInvalidTokenError
from typing import Any, Dict

class JWTDecoder:
    def __init__(self, public_key: Any, client_id: str):
        # Initializes the JWTDecoder with the public key and client ID.
        self.public_key = public_key
        self.client_id = client_id

    def decode_jwt(self, id_token: str) -> Dict[str, Any]:
        # Check if the public key is provided
        if not self.public_key:
            logging.error("Public key is not set")
            raise ValueError("Public key is not set")

        # Check if the ID token is provided
        if not id_token:
            logging.error("ID token is None or empty")
            raise ValueError("ID token is None or empty")

        try:
            # Decode the JWT with the given public key, client ID, and allow some leeway for token expiration
            decoded_payload = decode(
                id_token,
                self.public_key,
                algorithms=['RS256'],
                audience=self.client_id,
                leeway=300
            )

            logging.debug(f"Decoded JWT payload: {decoded_payload}")
            return decoded_payload

        except JwtExpiredSignatureError:
            logging.error("ID token has expired")
            raise

        except JwtInvalidTokenError as e:
            logging.error(f"Invalid ID token: {e}")
            raise

        except Exception as e:
            logging.error(f"Unexpected error decoding JWT: {e}")
            raise
