from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def generate_aes_key(key_length=32):
    """
    Generate a unique and secure AES key of the specified length.
    :param key_length: Length of the AES key in bytes (default is 32 bytes for AES-256).
    :return: Secure AES key as a byte string.
    """
    # Generate a random seed
    seed = os.urandom(32)  # 32 bytes = 256 bits of randomness
    salt = os.urandom(16)  # Salt to ensure unique derivation
    
    # Use HKDF to derive a strong AES key
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        info=b"AES_KEY_GENERATION",  # Context information
        backend=default_backend()
    )
    key = hkdf.derive(seed)
    return key

