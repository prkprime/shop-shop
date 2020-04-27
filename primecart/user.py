class User():

    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def get_type(self):
        return self.user_type

    @staticmethod
    def validate_login(password_hash, password):
        return password_hash == password
