import jwt
from responseCode import Response


class CheckJWT:
    def __init__(self, token):
        self.__token = token

    def confirm_token(self, public_key, alg):
        try:
            decoded = jwt.decode(self.__token, public_key, algorithms=alg)
            return Response.VALID
        except jwt.ExpiredSignatureError:
            return Response.EXPIRED
        except jwt.InvalidTokenError:
            return Response.INVALID