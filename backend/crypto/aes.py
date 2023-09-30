from symmetric_interface import SymmetricInterface
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from symmetric_interface import AesMode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from Cryptodome.Util import Counter

class Aes(SymmetricInterface):
    def __init__(self, mode):
        self.key = None
        self.mode = mode

    def generate_aes_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32, #bytes
            salt=b'1',
            iterations=480000,
        )
        try:
            self.key = kdf.derive(os.urandom(32))
            return True
        except Exception as e:
            print("AES key derivation failure:", e)
            return False

    def encrypt(self, data):
        if self.mode == AesMode.GCM:
            cipher = AES.new(self.key, AES.MODE_GCM)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            IV = cipher.nonce
            return ciphertext,  IV, tag
        elif self.mode == AesMode.CBC:
            cipher = AES.new(self.key, AES.MODE_CBC)
            padded_data = pad(data, AES.block_size)
            ciphertext = cipher.encrypt(padded_data)
            IV = cipher.IV
            return ciphertext, IV
        elif self.mode == AesMode.ECB:
            cipher = AES.new(self.key, AES.MODE_ECB)
            padded_data = pad(data, AES.block_size)
            ciphertext = cipher.encrypt(padded_data)
            return ciphertext
        elif self.mode == AesMode.CTR:
            iv = b'InitializationVt'
            ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
            cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
            ciphertext = cipher.encrypt(data)
            # IV = b'InitializationVect'
            IV = cipher.nonce
            return ciphertext, ctr

    def decrypt(self, ciphertext, IV = None, tag=None):
        if self.key == 0:
            return 0
        if self.mode == AesMode.GCM:
            cipher = AES.new(self.key, AES.MODE_GCM, IV)
            try:
                plaintext = cipher.decrypt_and_verify(ciphertext, tag)
                return plaintext
            except Exception as e:
                print("\nAES decode error ", e)
                return None
        elif self.mode == AesMode.CBC:
            cipher = AES.new(self.key, AES.MODE_CBC, IV)
            try:
                plaintext = cipher.decrypt(ciphertext)
                unpadded_plaintext = unpad(plaintext, AES.block_size)
                return unpadded_plaintext
            except Exception as e:
                print("\nAES decode error ", e)
                return None
        elif self.mode == AesMode.CTR:
            cipher = AES.new(self.key, AES.MODE_CTR, counter=IV)
            try:
                plaintext = cipher.decrypt(ciphertext)
                return plaintext
            except Exception as e:
                print("\nAES decode error ", e)
                return None
        elif self.mode == AesMode.ECB:
            cipher = AES.new(self.key, AES.MODE_ECB)
            try:
                plaintext = cipher.decrypt(ciphertext)
                plaintext = unpad(plaintext, AES.block_size)
                return plaintext
            except Exception as e:
                print("\nAES decode error ", e)
                return None


if __name__ == '__main__':
    aes_instance = Aes(AesMode.CTR)
    aes_instance.generate_aes_key()
    print(aes_instance.mode)
    input = "aaaaaaaaaaa"
    print(input)
    ciphertext, IV = aes_instance.encrypt(input.encode("utf-8"))
    print(aes_instance.decrypt(ciphertext, IV))
