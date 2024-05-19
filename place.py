import numpy as np
import pickle
from architect import Architect
# todo count the number of tiles in the canvas


class Place:
    def __init__(self, rows=14, cols=20, minutes_cooldown=2,
                 path="data/place.pkl"):
        self.rows = rows
        self.cols = cols
        self.minutes_cooldown = minutes_cooldown
        self.path = path
        self.default_char = "➕"
        self.digits = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        self.origin_character = "🛜"
        self.grid = None  # contains the player ids
        self.load_grid()

    def reset_grid(self):
        """Reset the grid to zeros"""
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        self.save_grid()

    def load_grid(self):
        """Load the grid from the place.pkl file. If the file does not exist, create a new grid."""
        try:
            with open(self.path, "rb") as f:
                self.grid = np.array(pickle.load(f))
        except FileNotFoundError:
            self.reset_grid()

    def save_grid(self):
        """Save the grid to the place.pkl file"""
        with open(self.path, "wb") as f:
            pickle.dump(self.grid.tolist(), f)

    def swap_pixel(self, x, y, user_id):
        """Swap the tile at the given coordinates"""
        x = np.clip(x, -self.rows, self.rows - 1)
        y = np.clip(y, -self.cols, self.cols - 1)
        if self.grid[x][y] == user_id:
            self.grid[x][y] = 0
        else:
            self.grid[x][y] = user_id
        self.save_grid()

    def __repr__(self):
        """Return a string representation of the grid"""
        architect = Architect()
        out = ""
        for j in reversed(range(self.cols)):
            out += self.digits[j % 10]
            for i in range(self.rows):
                if self.grid[i][j] == 0:
                    out += self.default_char
                else:
                    user_id = self.grid[i][j]
                    out += architect.get_user_emoji(user_id)
            out += "\n"
        out += self.origin_character
        for i in range(self.rows):
            out += self.digits[i % 10]
        return out
