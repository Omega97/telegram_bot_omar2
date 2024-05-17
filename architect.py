import os
import pickle


class Architect:
    def __init__(self):
        self.data_dir = "data"
        self.user_file = "data/user.pkl"
        self.build_env()

    def build_env(self):
        # create data directory
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # create user.pkl file
        if not os.path.exists(self.user_file):
            with open(self.user_file, "wb") as f:
                pickle.dump(dict(), f)
        return self

    def get_users(self) -> dict:
        with open(self.user_file, "rb") as f:
            users = pickle.load(f)
        return users

    def add_user(self, user_id, user_name):
        with open(self.user_file, "rb") as f:
            users = pickle.load(f)

        users[user_id] = user_name

        with open(self.user_file, "wb") as f:
            pickle.dump(users, f)
