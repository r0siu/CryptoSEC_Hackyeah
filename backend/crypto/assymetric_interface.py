class AssymetricInterface:
    def generate_key(self):
        """Generate assymetric key, store in class instance private and public key"""
        pass

    def generate_certificate(self):
        """Generate x509 certificate, store in class instance"""
        pass

    def load_certificate(self, path):
        """Load certificate from path"""
        pass

    def verify_certificate(self, certificate_data):
        """Verify certificate signature"""

    def load_private_key(self, private_key_data):
        """Load private key to class instance"""

    def generate_signature(self, input_data):
        """generate signature with prviate key, return signature"""

    def verify_signature(self, signature, data):
        """verify signature, return verification status"""

    def save_private_key_to_file(self):
        """save private key to .pem file"""