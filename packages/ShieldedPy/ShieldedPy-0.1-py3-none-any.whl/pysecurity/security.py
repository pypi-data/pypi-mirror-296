import hashlib
import hmac
import jwt
from cryptography.fernet import Fernet
from passlib.context import CryptContext


class SecurityManager:
    def __init__(self, secret_key, algorithm='HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.cipher_suite = Fernet(Fernet.generate_key())
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Password Handling
    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return self.password_context.hash(password)

    def verify_password(self, hashed_password: str, password: str) -> bool:
        """Verify a password."""
        return self.password_context.verify(password, hashed_password)

    # Token Management
    def create_token(self, payload: dict) -> str:
        """Create a JWT token."""
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def validate_token(self, token: str) -> dict:
        """Validate a JWT token."""
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    # Encryption/Decryption
    def encrypt(self, data: str) -> str:
        """Encrypt data."""
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data."""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
