import jwt


class GenJWT:
    def __init__(self, user_id, perm, exp_time):
        self.__payload = {'id': user_id,
                          'perm': perm,
                          'exp': exp_time}

    def generate_token(self, alg, private_key):
        gen_token = jwt.encode(self.__payload, private_key, algorithm=alg)
        return gen_token

