from backend.crypto.rsa import Rsa
from backend.jwt.JWTGenerator import JWTGenerator
from backend.jwt.JWTValidator import JWTValidator
from backend.users.userRepository import UserRepository
from datetime import datetime

class AuthenticationService:

    def __init__(self):
        rsa = Rsa("rsa instance")
        rsa.generate_key()
        self._jwtGenerator = JWTGenerator(rsa.rsa_private_key)
        self._jwtValidator = JWTValidator(rsa.rsa_public_key)
        self._userRepository = UserRepository()
        self._HALF_HOUR_IN_MS = 1_800_000

    def authenticate_user(self, username, password):
        foundUser = self._userRepository.get_user_by_username(username)
        jwtExpTime = self._get_current_time_ms() + self._HALF_HOUR_IN_MS
        return self._jwtGenerator.generate_token(foundUser.user_id, foundUser.permission, jwtExpTime)

    def validate_token(self, jwt):
        self._jwtValidator.validate_token(jwt)

    def _get_current_time_ms(self):
        current_datetime = datetime.now()
        current_time_ms = int(current_datetime.timestamp() * 1000)
        return current_time_ms
