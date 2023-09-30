from enum import Enum

class AesMode(Enum):
    GCM = 1
    CTR = 2
    CBC = 3
    ECB = 4


class SymmetricInterface:
    def generate_aes_key(self):
        """Generate AES key, for example pass random number to PBKDF2HMAC function"""
        pass

    def import_aes_key(self, aes_key_data):
        pass

    def encrypt(self, data):
        """Encrypt data, return ciphertext and IV eventually"""

    def decrypt(self, key, ciphertext, IV):
        """decrypt passed ciphertext with key"""
