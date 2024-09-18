# pysecurity

`pysecurity` is a simple library for managing security tasks such as password hashing, token management, and data encryption.

## Installation

You can install `pysecurity` using pip:

```bash
pip install pysecurity
```

## Usage

from pysecurity import SecurityManager

# Initialize SecurityManager
security = SecurityManager(secret_key='your-secret-key')

# Password Handling
hashed_password = security.hash_password('mypassword')
is_valid = security.verify_password(hashed_password, 'mypassword')

# Token Management
token = security.create_token({'user_id': 123})
data = security.validate_token(token)

# Encryption/Decryption
encrypted_data = security.encrypt('sensitive data')
decrypted_data = security.decrypt(encrypted_data)
