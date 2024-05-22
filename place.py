import numpy as np
import pickle
from architect import Architect


PLACE_PATHS = {"default": "data/place.pkl",
               "friends": "data/place_friends.pkl"}
MINUTES_COOLDOWN = 3
CANVAS_DEFAULT_SHAPE = (14, 20)


class Place:
    def __init__(self, rows=CANVAS_DEFAULT_SHAPE[0],
                 cols=CANVAS_DEFAULT_SHAPE[1],
                 minutes_cooldown=MINUTES_COOLDOWN,
                 canvas="default"):
        self.rows = rows
        self.cols = cols
        self.minutes_cooldown = minutes_cooldown
        self.canvas = canvas
        self.path = PLACE_PATHS[self.canvas]
        self.default_char = "➕"
        self.digits = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣",
                       "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        self.origin_character = "🌠"
        self.canvas = None  # contains the player ids
        self.load_grid()

    def _create_canvas(self, file):
        """Create new canvas"""
        self.canvas = np.array(pickle.load(file), dtype=np.int64)
        self.rows, self.cols = self.canvas.shape      # todo check

    def reset_grid(self):
        """Reset the grid to zeros"""
        self.canvas = np.zeros((self.rows, self.cols), dtype=np.int64)
        self.save_grid()

    def load_grid(self):
        """Load the grid from the place.pkl file. If the file does not exist, create a new grid."""
        try:
            with open(self.path, "rb") as f:
                self._create_canvas(f)
        except FileNotFoundError:
            self.reset_grid()

    def save_grid(self):
        """Save the grid to the place.pkl file"""
        with open(self.path, "wb") as f:
            pickle.dump(self.canvas.tolist(), f)

    def swap_pixel(self, x, y, user_id):
        """Swap the tile at the given coordinates"""
        x = np.clip(x, -self.rows, self.rows - 1)
        y = np.clip(y, -self.cols, self.cols - 1)
        if self.canvas[x][y] == user_id:
            self.canvas[x][y] = 0
        else:
            self.canvas[x][y] = user_id
        self.save_grid()

    def count_tiles(self):
        """Return a dictionary with the number of tiles for each user"""
        count = dict()
        for i in range(self.rows):
            for j in range(self.cols):
                user_id = self.canvas[i][j]
                if user_id != 0:
                    count[user_id] = count.get(user_id, 0) + 1
        return count

    def __repr__(self):
        """Return a string representation of the grid"""
        architect = Architect()
        out = ""
        for j in reversed(range(self.cols)):
            out += self.digits[j % 10]
            for i in range(self.rows):
                if self.canvas[i][j] == 0:
                    out += self.default_char
                else:
                    user_id = self.canvas[i][j]
                    out += architect.get_user_emoji(user_id)
            out += "\n"
        out += self.origin_character
        for i in range(self.rows):
            out += self.digits[i % 10]
        return out
