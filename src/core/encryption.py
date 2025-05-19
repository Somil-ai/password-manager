from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class PasswordEncryption:
    """Class handling encryption and decryption of passwords"""
    
    def __init__(self, master_password):
        """Initialize encryption with a master password"""
        self.salt = self._get_or_create_salt()
        self.key = self._derive_key(master_password)
        self.fernet = Fernet(self.key)
    
    def _get_or_create_salt(self):
        """Get existing salt or create a new one if it doesn't exist"""
        salt_file = os.path.join(os.path.expanduser("~"), ".securevault", "salt")
        os.makedirs(os.path.dirname(salt_file), exist_ok=True)
        
        if os.path.exists(salt_file):
            with open(salt_file, "rb") as f:
                return f.read()
        else:
            salt = os.urandom(16)
            with open(salt_file, "wb") as f:
                f.write(salt)
            return salt
    
    def _derive_key(self, password):
        """Derive an encryption key from the master password"""
        password_bytes = password.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def encrypt(self, password):
        """Encrypt a password"""
        return self.fernet.encrypt(password.encode()).decode()
    
    def decrypt(self, encrypted_password):
        """Decrypt an encrypted password"""
        try:
            return self.fernet.decrypt(encrypted_password.encode()).decode()
        except Exception:
            return None
    
    def validate_master_password(self, password):
        """Validate if the provided master password is correct"""
        test_key = self._derive_key(password)
        test_fernet = Fernet(test_key)
        
        # Try to decrypt a known encrypted value
        # This is just a placeholder implementation
        # In a real app, you would decrypt a stored test value
        try:
            test_fernet.decrypt(self.fernet.encrypt(b"test"))
            return True
        except Exception:
            return False