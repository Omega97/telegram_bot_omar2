"""
This is the Architect class. It is used to manage the users.
"""
import os
import hashlib
from time import gmtime, strftime
import numpy as np
from scripts.utils import DEFAULT_EMOJI, read_user_csv_file, write_user_csv_file
import cv2
from typing import List


class Architect:
    """Class to manage the users"""

    def __init__(self, data_dir="DATA"):
        # directories
        self.data_dir = data_dir
        self.private_data_dir = os.path.join(data_dir, "PRIVATE")
        self.canvases_dir = os.path.join(data_dir, "canvases")
        self.users_dir = os.path.join(self.private_data_dir, "users")
        self.photos_dir = os.path.join(self.private_data_dir, "photos")
        self.directories = (self.data_dir, self.canvases_dir, self.users_dir, self.photos_dir)

        # attributes
        self.user_info = dict()
        self.default_emoji = DEFAULT_EMOJI

        # build environment
        self._build_env()
        self._load_user_info()

    def get_user_message_path(self):
        """Get the file where the user messages are stored"""
        return os.path.join(self.private_data_dir, "user_messages.txt")

    def get_user_ids(self) -> tuple:
        """get tuple of all user ids"""
        return tuple(self.user_info.keys())

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
        for file_name in os.listdir(self.users_dir):
            if file_name.endswith('.csv'):
                user_id = int(file_name.split('.')[0])
                path = os.path.join(self.users_dir, file_name)
                self.user_info[user_id] = read_user_csv_file(path)

    def save_user_info(self):
        """Save the users to the user.pkl file"""
        for user_id in self.user_info:
            path = f'{self.users_dir}/{user_id}.csv'
            write_user_csv_file(path, self.user_info[user_id])

    def _build_env(self, verbose=True):
        # create directories
        for path in self.directories:
            if not os.path.exists(path):
                if verbose:
                    print(f">>> Creating directory: {path}")
                os.makedirs(path)

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
        else:
            print(f"User {user_name} ({user_id}) already exists")

    def get_user_name(self, user_id) -> str:
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
        v = [user_id for user_id in self.user_info if self.get_item(user_id, "santa", False)]
        return tuple(v)

    def get_gems(self, user_id):
        """Get the number of gems for a user"""
        return self.get_item(user_id, "gems", 0)

    def increase_gems(self, user_id, n_gems):
        """Increase the number of gems for a user"""
        assert n_gems >= 0, "Gems must be greater than zero"
        n = self.get_gems(user_id) + n_gems
        self.set_item(user_id, "gems", n)
        self.save_user_info()

    def decrease_gems(self, user_id, n_gems):
        """Decrease the number of gems for a user"""
        assert n_gems >= 0, "Gems must be greater than zero"
        n = self.get_gems(user_id) - n_gems
        self.set_item(user_id, "gems", n)
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

    def get_gems_leaderboard(self):
        """Return the leaderboard for the number of gems for all users"""
        v = []
        for user_id in self.user_info:
            n_gems = self.get_gems(user_id)
            if n_gems:
                emoji = self.get_user_emoji(user_id)
                name = self.get_user_name(user_id)
                v.append((name, emoji, n_gems))
        v.sort(key=lambda x: x[2], reverse=True)
        names, emojis, n_gems = zip(*v)
        return names, emojis, n_gems

    def get_admins(self) -> tuple:
        """get a tuple of all the admin ids"""
        return tuple([user_id for user_id in self.user_info if self.get_item(user_id, "admin", False)])

    def get_user_messages(self) -> list:
        """Get the last user message"""
        path = self.get_user_message_path()
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read().splitlines()
        else:
            return []

    def save_user_message(self, message, encoding="utf-8"):
        """Set the last user message"""
        path = self.get_user_message_path()
        if os.path.exists(path):
            with open(path, "a", encoding=encoding) as f:
                f.write(message + "\n")
        else:
            with open(path, "w", encoding=encoding) as f:
                f.write(message + "\n")

    def get_canvas_name(self, user_id):
        """Get the canvas for a user"""
        return self.get_item(user_id, "canvas", "default")

    def set_canvas(self, user_id, canvas: str):
        """Set the canvas for a user"""
        self.set_item(user_id, "canvas", canvas)
        self.save_user_info()

    def is_admin(self, user_id):
        """Return True if user is admin, else False """
        return self.get_item(user_id, 'admin', False)

    def get_admin_ids(self):
        """Return a list of admin ids"""
        return tuple([user_id for user_id in self.user_info if self.get_item(user_id, 'admin', False)])

    def set_user_emoji(self, user_id, emoji):
        """Set the emoji for a user"""
        self.set_item(user_id, "emoji", emoji)

    def smart_id_search(self, s: str) -> list:
        """Find all the users that contain the string s in their name"""
        s = s.lower()
        user_ids = self.get_user_ids()
        user_names = [self.get_user_name(user_id).lower() for user_id in user_ids]
        return [user_id for user_id, user_name in zip(user_ids, user_names) if s in user_name]

    def get_canvas_names(self):
        """Return the names of all the canvas files"""
        file_names = os.listdir(self.canvases_dir)
        file_names = [canvas_name for canvas_name in file_names if canvas_name.endswith('.csv')]
        return file_names

    def get_photo_names(self):
        """Return the names of all the photo files"""

        if not os.path.exists(self.photos_dir):
            return []
        else:
            return os.listdir(self.photos_dir)

    def get_photo(self, photo_name):
        """Return the png/jpg/jpeg photo file"""
        path = os.path.join(self.photos_dir, photo_name)
        return cv2.imread(path)

    def _get_active_santa_file_name(self):
        """Get the filename for the list of santas that have already checked the receiver this year"""
        year = strftime("%Y", gmtime())
        santas = self.get_santas()
        string = f'{year} {santas}'
        sha256_hash = hashlib.sha256(string.encode('utf-8')).hexdigest()
        return f'data/active_santas/{sha256_hash[:16]}.txt'

    def get_active_santas_ids(self) -> List[int]:
        """Get the list of the ids of santas that
        have already checked the receiver this year."""

        # check if the file in the filename exists
        filename = self._get_active_santa_file_name()
        if not os.path.exists(filename):
            # create an empty file, and all the necessary directories
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                f.write('')

        # read the file
        with open(filename, 'r') as f:
            text = f.read()
            active_santas = text.splitlines()
            active_santas = [int(santa) for santa in active_santas if santa]

        return active_santas

    def add_active_santa(self, santa):
        """Add a santa to the list of santas that have already checked the receiver this year"""
        filename = self._get_active_santa_file_name()
        active_santas = self.get_active_santas_ids()
        if santa not in active_santas:
            with open(filename, 'a') as f:
                f.write(f'{santa}\n')
