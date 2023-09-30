import jwt


class CheckJWT:
    def __init__(self, token):
        self.__token = token

    def confirm_token(self, public_key, alg):
        try:
            decoded = jwt.decode(self.__token, public_key, algorithms=alg)
            print("Token is correct.")
        except jwt.ExpiredSignatureError:
            print("Token expired.")
        except jwt.InvalidTokenError:
            print("Invalid token")