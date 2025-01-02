import numpy as np


class TankTeamTactics:
    def __init__(self, size:tuple):
        self.info = dict()
        self.size = size

    def get_field(self):
        mat = np.zeros(self.size, dtype=int)
        for player_id in self.info:
            x = self.info[player_id]['x']
            y = self.info[player_id]['y']
            mat[x, y] = player_id
        return mat

    def add_player(self, player_id):
        self.info[player_id] = dict()
