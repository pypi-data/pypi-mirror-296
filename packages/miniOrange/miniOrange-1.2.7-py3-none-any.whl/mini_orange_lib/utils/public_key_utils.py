import logging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def load_public_key(pem_data: str):
    try:
        # Convert the PEM data to bytes
        pem_bytes = pem_data.encode('utf-8')
        logging.debug(f"Loading public key from PEM data")
        # Load the public key from PEM data
        public_key = load_pem_public_key(pem_bytes, backend=default_backend())
        logging.debug("Public key successfully loaded")
        return public_key

    except ValueError as e:
        logging.error(f"Error loading public key: {e}")
        raise ValueError(f"Failed to load public key: {e}")
    except Exception as e:
        logging.error(f"Unexpected error loading public key: {e}")
        raise
