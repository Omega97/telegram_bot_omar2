import numpy as np
import pickle


class Place:
    def __init__(self, rows=20, cols=28, minutes_cooldown=2,
                 path="data/place.pkl"):
        self.rows = rows
        self.cols = cols
        self.minutes_cooldown = minutes_cooldown
        self.path = path
        self.default_char = "➕"
        self.grid = None
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

    def swap_pixel(self, x, y, char_id):
        """Swap the pixel at the given coordinates"""
        x = np.clip(x, -self.rows, self.rows - 1)
        y = np.clip(y, -self.cols, self.cols - 1)
        if self.grid[x][y] == 0:
            self.grid[x][y] = char_id
        else:
            self.grid[x][y] = 0
        self.save_grid()

    def __repr__(self):
        out = ""
        for j in reversed(range(self.cols)):
            for i in range(self.rows):
                if self.grid[i][j] == 0:
                    out += self.default_char
                else:
                    out += chr(self.grid[i][j])
            out += "\n"
        return out
