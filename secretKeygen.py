import secrets
import base64

secret_key = base64.b64encode(secrets.token_bytes(16)).decode('utf-8')  # Shorter key for prototyping
print(secret_key)