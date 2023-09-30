import jwt


class GenJWT:
    def __init__(self, user_id, exp_time):
        self.__payload = {'id': user_id,
                          'exp': exp_time}

    def generate_token(self, alg, private_key):
        token = jwt.encode(self.__payload, private_key, algorithm=alg)
        return token
