import numpy as np
import os
from architect import Architect


PLACE_DIR = "data/canvases"


class Place:
    def __init__(self, canvas_name="default.csv", shape=(14, 20), minutes_cooldown=3):
        self.minutes_cooldown = minutes_cooldown
        self.canvas_name = canvas_name
        if not canvas_name.endswith(".csv"):
            self.canvas_name += ".csv"
        self.default_char = "➕"
        self.digits = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣",
                       "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        self.origin_character = "🌠"
        self.canvas = None  # contains the player ids
        self.load_canvas(shape)

    def get_path(self):
        return os.path.join(PLACE_DIR, f"{self.canvas_name}")

    def read_canvas(self):
        """Read the canvas info from a file"""
        print(f'Reading canvas "{self.canvas_name}" from file...')

        with open(self.get_path(), "r", encoding='utf-8') as f:
            v = [list(map(int, line.strip().split(','))) for line in f]
            self.canvas = np.array(v, dtype=np.int64)

    def save_canvas(self):
        """Save the canvas by overwriting the file"""
        with open(self.get_path(), "w", encoding='utf-8') as f:
            for row in self.canvas:
                s = ','.join(map(str, row))
                f.write(f'{s}\n')

    def reset_canvas(self, shape):
        """Reset the canvas to zeros"""
        self.canvas = np.zeros(shape, dtype=np.int64)
        self.save_canvas()

    def load_canvas(self, shape):
        """Load the canvas from the file. If the file does not exist, create a new canvas."""
        try:
            # read the canvas from the file
            self.read_canvas()
        except FileNotFoundError:
            # create a new canvas
            self.reset_canvas(shape)

    def get_canvas_shape(self):
        """Return the shape of the canvas"""
        return self.canvas.shape

    def swap_pixel(self, x, y, user_id):
        """Swap the tile at the given coordinates"""
        rows, cols = self.get_canvas_shape()
        x = np.clip(x, -rows, rows - 1)
        y = np.clip(y, -cols, cols - 1)
        if self.canvas[x][y] == user_id:
            self.canvas[x][y] = 0
        else:
            self.canvas[x][y] = user_id
        self.save_canvas()

    def count_tiles(self):
        """Return a dictionary with the number of tiles for each user"""
        rows, cols = self.get_canvas_shape()
        count = dict()
        for i in range(rows):
            for j in range(cols):
                user_id = self.canvas[i][j]
                if user_id != 0:
                    count[user_id] = count.get(user_id, 0) + 1
        return count

    def __repr__(self):
        """Return a string representation of the canvas"""
        architect = Architect()
        rows, cols = self.get_canvas_shape()
        out = ""
        for j in reversed(range(cols)):
            out += self.digits[j % 10]
            for i in range(rows):
                if self.canvas[i][j] == 0:
                    out += self.default_char
                else:
                    user_id = self.canvas[i][j]
                    out += architect.get_user_emoji(user_id)
            out += "\n"
        out += self.origin_character
        for i in range(rows):
            out += self.digits[i % 10]
        return out
