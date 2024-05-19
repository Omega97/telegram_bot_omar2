import os
import pickle


class Architect:
    """Class to manage the users"""
    def __init__(self):
        self.data_dir = "data"
        self.user_file = "data/user.pkl"
        self.user_info = None
        self._build_env()
        self._load_user_info()

    def __getitem__(self, item):
        return self.user_info[item]

    def _load_user_info(self):
        """Load the users from the user.pkl file."""
        with open(self.user_file, "rb") as f:
            self.user_info = pickle.load(f)

    def save_user_info(self):
        """Save the users to the user.pkl file."""
        if self.user_info is not None:
            with open(self.user_file, "wb") as f:
                pickle.dump(self.user_info, f)

    def _build_env(self):
        # create data directory
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # create user.pkl file if not exists
        if not os.path.exists(self.user_file):
            self.user_info = dict()
            self.save_user_info()

    def get_user_info(self) -> dict:
        """Return the users from the user.pkl file."""
        return self.user_info

    def add_user(self, user_id, user_name):
        """Add a user to the user.pkl file."""
        if user_name is None:
            print('User name is None')
            return
        if user_id in self.user_info:
            print(f"\n>>>User {user_id} {user_name} already exists")
            return

        print(f"\n>>>Adding user {user_id} {user_name}")

        # create new user if not exists
        if user_id not in self.user_info:
            # default user info
            self.user_info[user_id] = {"username": user_name,
                                       "emoji": "👤",
                                       "achievements": dict()}
            self.save_user_info()

    def del_user(self, user_id):
        """Delete a user from the user.pkl file."""
        del self.user_info[user_id]
        self.save_user_info()

    def get_user_names(self) -> list:
        """Return the usernames from the user.pkl file."""
        return [user["username"] for user in self.user_info.values()]

    def set_emoji(self, user_id, emoji):
        """Set the emoji for a user."""
        self.user_info[user_id]["emoji"] = emoji
        self.save_user_info()

    def get_user_emoji(self, user_id):
        """Get the emoji for a user"""
        print(self.user_info[user_id])
        return self.user_info[user_id]["emoji"]

    def get_last_place_time(self, user_id):
        """Get the last time the place was used."""
        return self.user_info[user_id].get("last_place_time", None)

    def set_last_place_time(self, user_id, time):
        """Set the last time the place was used."""
        self.user_info[user_id]["last_place_time"] = time
        self.save_user_info()
