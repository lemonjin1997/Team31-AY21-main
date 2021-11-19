# Importing open-source API(s)
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, name, id, role):
        self.name = name
        self.id = id
        self.role = role

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
