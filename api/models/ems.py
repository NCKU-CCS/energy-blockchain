
users = []


class UserModel:
    name = ''
    email = ''
    password = ''

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def add_user(self):
        users.append(self)

    @staticmethod
    def get_user(name):
        find = [item for item in users if item.name == name]
        if len(find) == 0:
            return None
        return find[0]

    @staticmethod
    def delete_user(name):
        global users
        users = [item for item in users if item.name != name]

    @staticmethod
    def get_all_user():
        return users


