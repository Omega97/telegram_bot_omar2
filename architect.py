"""
This is the Architect class. It is used to manage the users.
"""
import os
import pickle
import numpy as np


class Architect:
    """Class to manage the users"""

    def __init__(self):
        self.data_dir = "data"
        self.user_file = "data/user.pkl"
        self.user_message_path = "data/user_message.pkl"
        self.user_info = None
        self.default_emoji = ["⬜️", "🟥", "🟧", "🟨", "🟩", "🟦", "🟪",
                              "⚪", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣"]
        self._build_env()
        self._load_user_info()

    def get_item(self, user_id, item, default):
        """Get a key-value pair for a user"""
        return self.user_info[user_id].get(item, default)

    def set_item(self, user_id, key, value):
        """Set a key-value pair for a user"""
        self.user_info[user_id][key] = value
        self.save_user_info()

    def del_item(self, user_id, key):
        """Delete a key-value pair for a user"""
        del self.user_info[user_id][key]
        self.save_user_info()

    def get_random_emoji(self):
        """Return a random emoji from the default_emoji list"""
        i = np.random.randint(len(self.default_emoji))
        return self.default_emoji[i]

    def _load_user_info(self):
        """Load the users from the user.pkl file"""
        with open(self.user_file, "rb") as f:
            self.user_info = pickle.load(f)

    def save_user_info(self):
        """Save the users to the user.pkl file"""
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
        """Return the users from the user.pkl file"""
        return self.user_info

    def add_user(self, user_id, user_name):
        """Add a user to the user.pkl file"""
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
            self.user_info[user_id] = dict()
            self.set_item(user_id, "username", user_name)
            self.set_item(user_id, "emoji", self.get_random_emoji())
            self.set_item(user_id, "achievements", dict())
            self.save_user_info()

    def get_user_name(self, user_id):
        """Get the name of a user"""
        return self.get_item(user_id, "username", "None")

    def get_user_emoji(self, user_id):
        """Get the emoji for a use"""
        return self.user_info[user_id].get("emoji", self.get_random_emoji())

    def del_user(self, user_id):
        """Delete a user from the user.pkl file"""
        del self.user_info[user_id]
        self.save_user_info()

    def get_user_names(self) -> list:
        """Return the usernames from the user.pkl file"""
        return [user["username"] for user in self.user_info.values()]

    def set_emoji(self, user_id, emoji):
        """Set the emoji for a user"""
        self.set_item(user_id, "emoji", emoji)
        self.save_user_info()

    def get_last_place_time(self, user_id):
        """Get the last time the place was used"""
        return self.get_item(user_id, "last_place_time", None)

    def set_last_place_time(self, user_id, time):
        """Set the last time the place was used"""
        self.set_item(user_id, "last_place_time", time)
        self.save_user_info()

    def get_place_tiles_count(self, user_id) -> int:
        """Get the number of tiles placed by a user"""
        return self.user_info[user_id].get("tiles_count", 0)

    def add_place_tiles_count(self, user_id, count=1):
        """Add the number of tiles placed by a user"""
        n = self.get_place_tiles_count(user_id) + count
        self.set_item(user_id, "tiles_count", n)
        self.save_user_info()

    def set_admin(self, user_id, admin=True):
        """Set the admin flag for a user"""
        self.set_item(user_id, "admin", admin)
        self.save_user_info()

    def set_santa(self, user_id, santa=True):
        """Set the santa flag for a user"""
        self.set_item(user_id, "santa", santa)
        self.save_user_info()

    def get_santas(self) -> tuple:
        """Return the user ids of the Santas"""
        return tuple([user_id for user_id in self.user_info if self.get_item(user_id, "santa", False)])

    def get_points(self, user_id):
        """Get the number of points for a user"""
        return self.get_item(user_id, "points", 0)

    def increase_points(self, user_id, points):
        """Increase the number of points for a user"""
        assert points > 0, "Points must be greater than zero"
        n = self.get_points(user_id) + points
        self.set_item(user_id, "points", n)
        self.save_user_info()

    def get_tile_leaderboard(self):
        """Return the leaderboard for the number of tiles placed by each user"""
        v = []
        for user_id in self.user_info:
            n_tiles = self.get_place_tiles_count(user_id)
            if n_tiles:
                emoji = self.get_user_emoji(user_id)
                name = self.get_user_name(user_id)
                v.append((name, emoji, n_tiles))
        v.sort(key=lambda x: x[2], reverse=True)
        names, emojis, tiles = zip(*v)
        return names, emojis, tiles

    def get_leaderboard(self):
        """Return the leaderboard for the number of points for all users"""
        v = []
        for user_id in self.user_info:
            points = self.get_points(user_id)
            if points:
                emoji = self.get_user_emoji(user_id)
                name = self.get_user_name(user_id)
                v.append((name, emoji, points))
        v.sort(key=lambda x: x[2], reverse=True)
        names, emojis, points = zip(*v)
        return names, emojis, points

    def get_admins(self) -> tuple:
        """get a tuple of all the admin ids"""
        return tuple([user_id for user_id in self.user_info if self.get_item(user_id, "admin", False)])

    def set_last_user_message(self, user_id, message):
        """Set the last user message"""
        with open(self.user_message_path, "wb") as f:
            pickle.dump((user_id, message), f)

    def get_last_user_message(self) -> tuple:
        """Get the last user message"""
        if os.path.exists(self.user_message_path):
            with open(self.user_message_path, "rb") as f:
                return pickle.load(f)
        else:
            return None, None

    def get_canvas(self, user_id):
        """Get the canvas for a user"""
        return self.get_item(user_id, "canvas", "default")

    def set_canvas(self, user_id, canvas):
        """Set the canvas for a user"""
        self.set_item(user_id, "canvas", canvas)
        self.save_user_info()
