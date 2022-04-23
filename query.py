from coord import Coord
from helper import map_helper, agent_helper
from constant import Action, Direction
class query:
    def visited(self, matrix_map, coord_rel):
        if matrix_map[coord_rel.y][coord_rel.x][4] == 'S':
            return True
        return False

    def wumpus(self, matrix_map, coord_rel):
        if matrix_map[coord_rel.y][coord_rel.x][4] == 'W':
            return True
        return False
    
    def confundus(self, matrix_map, coord_rel):
        if matrix_map[coord_rel.y][coord_rel.x][4] == 'O':
            return True
        return False
    
    def tingle(self, matrix_map, coord_rel):
        if matrix_map[coord_rel.y][coord_rel.x][2] == 'T':
            return True
        return False

    def glitter(self, matrix_map, coord_rel):
        if matrix_map[coord_rel.y][coord_rel.x][6] == '*':
            return True
        return False

    def stench(self, matrix_map, coord_rel):
        if matrix_map[coord_rel.y][coord_rel.x][1] == '=':
            return True
        return False
    
    def safe(self, matrix_map, coord_rel):
        if self.wumpus(matrix_map, coord_rel) == False and self.confundus(matrix_map, coord_rel) == False:
            return True
        return False
    
    def wall(self, matrix_map, coord_rel):
        if matrix_map[coord_rel.y][coord_rel.x][0] == '#':
            return True
        return False

    def reborn(self,matrix_map, agent):
        coord_safe = map_helper.find_safe_cell(matrix_map)
        agent.x_abs = coord_safe.x
        agent.y_abs = coord_safe.y
        agent.dir_abs = Direction.NORTH

        agent.x_rel = 0
        agent.y_rel = 0
        agent.dir_rel = Direction.NORTH

        agent.sensorylist = map_helper.convert_cell_to_sensory_list(matrix_map[coord_safe.y][coord_safe.x])

    def move(self, matrix_map, agent, action):
        # update on absolute map
        # first determine the direction of agent
        if action == Action.TURNLEFT or action == Action.TURNRIGHT:
            agent.dir_abs = agent_helper.change_agent_direction(agent.dir_abs, action)
            agent.dir_rel = agent_helper.change_agent_direction(agent.dir_rel, action)
            map_helper.update_agent_dir_in_map(matrix_map, agent)

        elif action == Action.MOVEFORWARD:
            map_helper.update_agent_loc_in_map(matrix_map, agent)
    
        elif action == Action.SHOOT:
            map_helper.update_wumpus_in_map(matrix_map, agent)

        elif action == Action.PICKUP:
            map_helper.update_coin_in_map(matrix_map, agent)

        # update on relative map
        
    def reposition(self,matrix_map, agent):
        coord_safe = map_helper.find_safe_cell(matrix_map)
        agent.x_abs = coord_safe.x
        agent.y_abs = coord_safe.y
        agent.dir_abs = Direction.NORTH

        agent.x_rel = 0
        agent.y_rel = 0
        agent.dir_rel = Direction.NORTH

        agent.sensorylist = map_helper.convert_cell_to_sensory_list(matrix_map[coord_safe.y][coord_safe.x])

    def current(self, agent, coord_rel, dir_rel):
        if agent.x_rel == coord_rel.x and agent.y_rel == coord_rel.x and agent.dir_rel == dir_rel:
            return True
        return False
    
    def hasarrow(self, agent):
        if agent.hasarrow == True:
            return True
        return False

        