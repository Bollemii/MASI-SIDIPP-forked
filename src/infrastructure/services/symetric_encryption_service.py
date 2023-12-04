import Crypto.Cipher.AES
import Crypto.Random

from src.application.interfaces.isymetric_encryption_service import (
    ISymetricEncryptionService,
)


class SymetricEncryptionService(ISymetricEncryptionService):
    """Symetric Encryption Service"""

    def generate_key(self) -> bytes:
        return Crypto.Random.get_random_bytes(32)

    def encrypt(self, plaintext: str, key: bytes) -> tuple[bytes, str, str]:
        if plaintext is None or plaintext.strip() == "":
            raise ValueError("Plaintext cannot be empty", plaintext)

        if key is None or key.strip() == "":
            raise ValueError("Key cannot be empty", key)

        plaintext_bytes = plaintext.encode()
        cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(plaintext_bytes)

        return (cipher.nonce, tag, ciphertext)

    def decrypt(self, ciphertext: str, key: bytes, tag: str, nonce: bytes) -> str:
        if ciphertext is None or ciphertext.strip() == "":
            raise ValueError("Ciphertext cannot be empty", ciphertext)

        if key is None or key.strip() == "":
            raise ValueError("Key cannot be empty", key)

        if tag is None or tag.strip() == "":
            raise ValueError("Tag cannot be empty", tag)

        if nonce is None or nonce.strip() == "":
            raise ValueError("Nonce cannot be empty", nonce)

        cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_EAX, nonce)

        plaintext_bytes = cipher.decrypt_and_digest(ciphertext, tag)

        return plaintext_bytes.decode()
