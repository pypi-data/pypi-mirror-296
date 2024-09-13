import os

from cryptography.fernet import Fernet


class EncryptionHelper:
    def __init__(self, key: str = None):
        if key is None:
            key = os.getenv("PLURALLY_ENCRYPTION_KEY")
        if key is None:
            raise ValueError(
                "Should provide encryption key or set env variable PLURALLY_ENCRYPTION_KEY"
            )
        self.cipher = Fernet(key)

    def encrypt(self, plain_text: str) -> str:
        return self.cipher.encrypt(plain_text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        return self.cipher.decrypt(encrypted_text.encode()).decode()


def encrypt(val):
    return EncryptionHelper().encrypt(val)


def decrypt(val):
    return EncryptionHelper().decrypt(val)
