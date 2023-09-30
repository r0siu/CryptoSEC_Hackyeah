import assymetric_interface

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import utils

class ECDSA(assymetric_interface.AssymetricInterface):
    def __init__(self):
        # self.certificate_path = dir
        self.ecdsa_private_key = None
        self.ecdsa_public_key = None
        self.certificate = None

    def generate_key(self):
        self.ecdsa_private_key = ec.generate_private_key(
            curve=ec.SECP256R1(),
            backend=default_backend()
        )
        self.ecdsa_public_key = self.ecdsa_private_key.public_key()

    def load_certificate(self, path):
        with open(path, "rb") as cert_file:
            self.certificate_data = cert_file.read()
        try:
            self.certificate = x509.load_pem_x509_certificate(self.certificate_data, default_backend())
        except Exception as e:
            print("Certificate load failure:", e)

    def load_private_key(self, private_key_data):
        with open(private_key_data, 'rb') as key_file:
            private_key_pem = key_file.read()
            self.ecdsa_private_key = serialization.load_pem_private_key(
                private_key_pem,
                password=None,
                backend=default_backend()
            )
        self.ecdsa_public_key = self.ecdsa_private_key.public_key()
    def generate_signature(self, input_data):
        signature = self.ecdsa_private_key.sign(
            input_data.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return signature

    def verify_signature(self, signature, data):
        try:
            self.ecdsa_public_key.verify(
                signature,
                data.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

    def save_private_key_to_file(self, filename):
        try:
            with open(filename, 'wb') as key_file:
                private_key_pem = self.ecdsa_private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
                key_file.write(private_key_pem)
        except Exception as e:
            print(e)
