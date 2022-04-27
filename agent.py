from coord import Coord

class Agent:
    def __init__(self, coord_abs, dir_abs, coord_rel, dir_rel, sensorylist, hasarrow):
        self.x_abs = coord_abs.x
        self.y_abs = coord_abs.y
        self.dir_abs = dir_abs

        self.x_rel = coord_rel.x
        self.y_rel = coord_rel.y
        self.x_rel_temp = 21
        self.y_rel_temp = 21
        self.dir_rel = dir_rel

        self.sensorylist = sensorylist

        self.hasarrow = hasarrow
