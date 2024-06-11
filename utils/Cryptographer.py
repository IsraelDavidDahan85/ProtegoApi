import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ALGORITHM = hashes.SHA256()
KDF_LENGTH = 32
KDF_ITERATIONS = 120000
password = 'password'


def encrypt(plaintext: str) -> (str, str):
    # Derive a symmetric key using the passsword and a fresh random salt.
    salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=KDF_ALGORITHM, length=KDF_LENGTH, salt=salt,
        iterations=KDF_ITERATIONS)
    key = kdf.derive(password.encode("utf-8"))

    # Encrypt the message.
    f = Fernet(base64.urlsafe_b64encode(key))
    ciphertext = f.encrypt(plaintext.encode("utf-8"))
    ciphertext_str = base64.urlsafe_b64encode(ciphertext).decode("utf-8")
    salt_str = base64.urlsafe_b64encode(salt).decode("utf-8")
    return ciphertext_str, salt_str


def decrypt(ciphertext: str, salt: str) -> str:
    salt = base64.urlsafe_b64decode(salt.encode("utf-8"))
    ciphertext = base64.urlsafe_b64decode(ciphertext.encode("utf-8"))
    # Derive the symmetric key using the password and provided salt.
    kdf = PBKDF2HMAC(
        algorithm=KDF_ALGORITHM, length=KDF_LENGTH, salt=salt,
        iterations=KDF_ITERATIONS)
    key = kdf.derive(password.encode("utf-8"))

    # Decrypt the message
    f = Fernet(base64.urlsafe_b64encode(key))
    plaintext = f.decrypt(ciphertext)

    return plaintext.decode("utf-8")
