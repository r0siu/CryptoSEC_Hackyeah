import jwt
from responseCode import Response


class CheckJWT:
    def __init__(self, token):
        self.__data = {}
        self.__token = token

    def confirm_token(self, public_key, alg):
        try:
            decoded = jwt.decode(self.__token, public_key, algorithms=alg)
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

