from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
import random, os
from assymetric_interface import AssymetricInterface

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization



class Rsa(AssymetricInterface):
    def __init__(self, name):
        self.id = random.randint(0, 1000)
        self.name = name
        self.rsa_private_key = 0    # only for client
        self.rsa_private_key_bytes = 0
        self.rsa_public_key = 0     # only for server
        self.rsa_public_key_bytes = 0
        self.certificate = 0
        self.certificate_data = 0
        self.rsa_received_public_key = 0


    def generate_key(self):
        rsa_private_key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )
        with open('rsa/private_key_client.pem', 'w+b') as key_file:
            key_file.write(rsa_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        self.rsa_private_key = rsa_private_key
        self.rsa_public_key = self.rsa_private_key.public_key()
        self.rsa_private_key_bytes = self.rsa_private_key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        )

        self.rsa_public_key_bytes = self.rsa_public_key.public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )

    #
    # def generate_certificate(self):
    #     with open('rsa/private_key_client.pem', 'rb') as key_file:
    #         pem_data_client = key_file.read()
    #         private_key_client = serialization.load_pem_private_key(
    #         pem_data_client,
    #         password=None  # If your key is password-protected, provide the password here as bytes
    #     )
    #
    #     subject = x509.Name([
    #         x509.NameAttribute(NameOID.COUNTRY_NAME, "PL"),
    #         x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "malopolskie"),
    #         x509.NameAttribute(NameOID.LOCALITY_NAME, "Krakow"),
    #         x509.NameAttribute(NameOID.ORGANIZATION_NAME, "AGH"),
    #         x509.NameAttribute(NameOID.COMMON_NAME, "secure_channel.com"),
    #     ])
    #
    #     public_key = private_key_client.public_key()
    #     builder = x509.CertificateBuilder()
    #     builder = builder.subject_name(subject)
    #     builder = builder.issuer_name(subject)
    #     builder = builder.not_valid_before(datetime.datetime.utcnow())
    #     builder = builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    #     builder = builder.serial_number(x509.random_serial_number())
    #     builder = builder.public_key(public_key)
    #     builder = builder.add_extension(
    #         x509.BasicConstraints(ca=True, path_length=None), critical=True,
    #     )
    #     certificate = builder.sign(
    #         private_key=private_key_server, algorithm=hashes.SHA256(),
    #         backend=default_backend(),
    #     )
    #     with open('rsa/invalid_certificate.pem', 'wb') as cert_file:
    #         cert_file.write(certificate.public_bytes(
    #             encoding=serialization.Encoding.PEM
    #         ))

    def load_certificate(self, path):
        with open(path, "rb") as cert_file:
            self.certificate_data = cert_file.read()
        try:
            self.certificate = x509.load_pem_x509_certificate(self.certificate_data, default_backend())
        except Exception as e:
            print("Certificate load failure:", e)

    # def verify_certificate(self, cert_data):
    #     try:
    #         received_certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
    #     except Exception as e:
    #         print("Certificate load failure:", e)
    #
    #     try:
    #         self.rsa_public_key.verify(
    #             received_certificate.signature,
    #             received_certificate.tbs_certificate_bytes,
    #             padding.PKCS1v15(),
    #             hashes.SHA256()
    #         )
    #
    #     except Exception as e:
    #         print("\nCertificate verification failed ", e)
    #         return False
    #     self.rsa_received_public_key = received_certificate.public_key()
    #     return True


    def get_public_key_from_certificate(self, cert_data):
        try:
            received_certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
        except Exception as e:
            print("Certificate load failure:", e)
        self.rsa_received_public_key = received_certificate.public_key()

    # data should be encoded in utf-8 .encode('utf-8')
    def sign_with_rsa_key(self, data):
        signature = self.rsa_private_key.sign(data,
                                padding.PSS(
                                    mgf=padding.MGF1(hashes.SHA256()),
                                    salt_length=padding.PSS.MAX_LENGTH
                                ),
                                hashes.SHA256())
        return signature

    def verify_rsa_signature(self, signature, data):
        print(signature)
        print(data)
        try:
            self.rsa_public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False



if __name__ == "__main__":
    rsa_instance = Rsa("Rsa")
    rsa_instance.generate_key()

    with open('test.txt', 'r') as file:
        # Read the entire contents of the file into a string
        file_contents = file.read()
    signature = rsa_instance.sign_with_rsa_key(file_contents.encode('utf-8'))
    print(signature)
    print(rsa_instance.verify_rsa_signature(signature, file_contents.encode('utf-8')))
