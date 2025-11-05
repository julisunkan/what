import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def _get_encryption_key():
    secret = os.environ.get('ENCRYPTION_SECRET', 'dev-encryption-key-change-in-production')
    salt = b'whatsapp_bot_salt'
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret.encode()))
    return key

def encrypt_value(value):
    if not value:
        return None
    
    key = _get_encryption_key()
    f = Fernet(key)
    encrypted = f.encrypt(value.encode())
    return base64.urlsafe_b64encode(encrypted).decode('utf-8')

def decrypt_value(encrypted_value):
    if not encrypted_value:
        return None
    
    try:
        key = _get_encryption_key()
        f = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_value.encode('utf-8'))
        decrypted = f.decrypt(encrypted_bytes)
        return decrypted.decode('utf-8')
    except Exception:
        return None
