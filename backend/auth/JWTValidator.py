import jwt
from .responseCode import Response


class JWTValidator:
    def __init__(self, public_key):
        self.__public_key = public_key

    def validate_token(self, token):
        try:
            decoded = jwt.decode(token, self.__public_key, algorithms=["RS256"])
            self.__data = {}
            self.__extract_data(decoded)
            return Response.VALID
        except jwt.ExpiredSignatureError:
            return Response.EXPIRED
        except jwt.InvalidTokenError:
            return Response.INVALID

    def __extract_data(self, decoded):
        self.__data["id"] = decoded.get("id")
        self.__data["perm"] = decoded.get("perm")
        self.__data["exp"] = decoded.get("exp")


    def get_data(self):
        return self.__data

