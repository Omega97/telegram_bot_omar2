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

    def get_user_info(self) -> dict:
        """Return the users from the user.pkl file."""
        with open(self.user_file, "rb") as f:
            users = pickle.load(f)
        return users

    def add_user(self, user_id, user_name):
        """Add a user to the user.pkl file."""
        if user_name is not None:
            print(f"\n>>>Adding user {user_id} {user_name}")
            with open(self.user_file, "rb") as f:
                users = pickle.load(f)

            # create new user if not exists
            if user_id not in users:
                users[user_id] = {"username": user_name}
                with open(self.user_file, "wb") as f:
                    pickle.dump(users, f)
        else:
            print("User name cannot be None!")

    def del_user(self, user_id):
        """Delete a user from the user.pkl file."""
        with open(self.user_file, "rb") as f:
            users = pickle.load(f)
        del users[user_id]
        with open(self.user_file, "wb") as f:
            pickle.dump(users, f)

    def get_user_names(self) -> list:
        """Return the user names from the user.pkl file."""
        with open(self.user_file, "rb") as f:
            users = pickle.load(f)
        return [user["username"] for user in users.values()]
