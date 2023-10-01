from backend.users.User import User

# Mocked user repository
class UserRepository:
    def get_user_by_username(self, username):
        return User(1, "Admin")