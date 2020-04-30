class User():

    def __init__(self, username, user_type, customer_id):
        self.username = username
        self.user_type = user_type
        self.user_id = customer_id

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

    def get_int_id(self):
        return self.user_id

    @staticmethod
    def validate_login(password_hash, password):
        return password_hash == password
