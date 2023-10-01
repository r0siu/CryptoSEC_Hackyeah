import jwt


class JWTGenerator:
    def __init__(self, private_key):
        self.private_key = private_key

    # By default uses HS256
    def generate_token(self, user_id, perm, exp_time):
        payload = {'id': user_id,
                   'perm': perm,
                   'exp': exp_time}
        token = jwt.encode(payload, self.private_key)
        return token
