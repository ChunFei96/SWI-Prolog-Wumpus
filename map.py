from itertools import count
from random import  randint
import random
from helper import map_helper
from coord import Coord
from agent import Agent
from constant import Sensory, Direction

Y_COUNT = 6-1

class map:
      # init method or constructor
    def __init__(self,r_map,c_map,r_cell,c_cell):
        self.r_map = r_map
        self.c_map = c_map
        self.r_cell = r_cell
        self.c_cell = c_cell

    def map_generator_abs(self):
        self.matrix_map = [[ [1,2,3,4,5,6,7,'.','.'] for x in range(self.r_map)] for y in range(self.c_map)]
        # draw wall
        for x in range(self.r_map):
            for y in range(self.c_map):
                if y >= 1 and y <= 4:
                    self.matrix_map[y][0] = ['#','#','#','#','#','#','#','#','#']
                    self.matrix_map[y][6] = ['#','#','#','#','#','#','#','#','#']
                else:
                    self.matrix_map[y][x] = ['#','#','#','#','#','#','#','#','#']
                    self.matrix_map[y][x] = ['#','#','#','#','#','#','#','#','#']

        # generate Wumpus
        self.Wumpus_rand()

        # generate Portal
        self.Portal_rand()

        # generate Coin
        self.Coin_rand()

        # generate Agent
        self.Agent_rand()

        # update safe cell
        map_helper.update_safe_cell(self.matrix_map)

    def map_generator_rel(self):
        r_map_rel = 50
        c_map_rel = 50

        self.matrix_map_rel = [[ ['.','.','.',' ','?',' ','.','.','.'] for x in range(r_map_rel)] for y in range(c_map_rel)]

    def Wumpus_rand(self, isRand=False):
        if isRand == False:
            x = 1
            y = 3
        else:
            x, y = randint(1, 5), randint(1, 4)

        # update the current cell symbol 5 to W
        self.matrix_map[Y_COUNT-y][x][4] = 'W'

        # update the other cell sumbol 5 to ?
        xy_list_exclude_wumpus = set()
        xy_list_exclude_wumpus.add((x,y))
        map_helper.update_other_coord_in_matrix(self.matrix_map, '?', 4, xy_list_exclude_wumpus)
        
        # update the current cell symbol 4/6 to -
        self.matrix_map[Y_COUNT-y][x][3] = '-'
        self.matrix_map[Y_COUNT-y][x][5] = '-'

        # update the adjacent cells symbol 2 to =
        xy_list_exclude_stench = set()
        if map_helper.is_coord_in_matrix(self.matrix_map, x+1, y):
            self.matrix_map[Y_COUNT-y][x+1][1] = '='
            xy_list_exclude_stench.add((x+1,y))
        
        if map_helper.is_coord_in_matrix(self.matrix_map, x, y+1):
            self.matrix_map[Y_COUNT-y-1][x][1] = '='
            xy_list_exclude_stench.add((x,y-1))

        if map_helper.is_coord_in_matrix(self.matrix_map, x-1, y):
            self.matrix_map[Y_COUNT-y][x-1][1] = '='
            xy_list_exclude_stench.add((x-1,y))

        if map_helper.is_coord_in_matrix(self.matrix_map, x, y-1):
            self.matrix_map[Y_COUNT-y+1][x][1] = '='
            xy_list_exclude_stench.add((x,y+1))
        
        # update the other cell sumbol 2 to .
        map_helper.update_other_coord_in_matrix(self.matrix_map, '.', 1, xy_list_exclude_stench)

        self.wumpus_coord_abs = Coord(x,y)
        return self.wumpus_coord_abs

    def Portal_rand(self, isRand=False):
        xy_list_exclude_portal = set()
        self.portal_coord_abs_list = []
        for i in range(3):
            if isRand == False:
                if i == 0:
                    x = 5
                    y = 4
                elif i == 1:
                    x = 4
                    y = 4
                elif i == 2:
                    x = 2
                    y = 1
            else:
                x, y = randint(1, 5), randint(1, 4)

                while self.matrix_map[Y_COUNT-y][x][4] == 'O':
                    x, y = randint(1, 5), randint(1, 4)
                    continue

            # update the current cell symbol 5 to W
            if self.matrix_map[Y_COUNT-y][x][4] == 'W':
                self.matrix_map[Y_COUNT-y][x][4] = 'U'
            else:
                self.matrix_map[Y_COUNT-y][x][4] = 'O'

            # update the adjacent cells symbol 2 to =
            xy_list_exclude_tingle = set()
            if map_helper.is_coord_in_matrix(self.matrix_map, x+1, y):
                self.matrix_map[Y_COUNT-y][x+1][2] = 'T'
                xy_list_exclude_tingle.add((x+1,y))
            
            if map_helper.is_coord_in_matrix(self.matrix_map, x, y+1):
                self.matrix_map[Y_COUNT-y-1][x][2] = 'T'
                xy_list_exclude_tingle.add((x,y-1))

            if map_helper.is_coord_in_matrix(self.matrix_map, x-1, y):
                self.matrix_map[Y_COUNT-y][x-1][2] = 'T'
                xy_list_exclude_tingle.add((x-1,y))

            if map_helper.is_coord_in_matrix(self.matrix_map, x, y-1):
                self.matrix_map[Y_COUNT-y+1][x][2] = 'T'
                xy_list_exclude_tingle.add((x,y+1))
            
            # update the other cell sumbol 3 to .
            map_helper.update_other_coord_in_matrix(self.matrix_map, '.', 2, xy_list_exclude_tingle)
            
            xy_list_exclude_portal.add((x,y))
            self.portal_coord_abs_list.append(Coord(x,y))
            # update the current cell symbol 4/6 to -
            self.matrix_map[Y_COUNT-y][x][3] = '-'
            self.matrix_map[Y_COUNT-y][x][5] = '-'
        
        # update the other cell sumbol 5 to ?
        map_helper.update_other_coord_in_matrix(self.matrix_map, '?', 4, xy_list_exclude_portal)

        return self.portal_coord_abs_list

    def Coin_rand(self, isRand=False):
        if isRand == False:
            x = 5
            y = 2
        else:
            x, y = randint(1, 5), randint(1, 4)

        # update the current cell symbol 7 to *
        self.matrix_map[Y_COUNT-y][x][6] = '*'
        # update the other cell sumbol 7 to space '.'
        xy_list_exclude_coin = set()
        xy_list_exclude_coin.add((x,y))
        map_helper.update_other_coord_in_matrix(self.matrix_map, '.', 6, xy_list_exclude_coin)

        # update the current cell symbol 4/6 to -
        self.matrix_map[Y_COUNT-y][x][3] = '-'
        self.matrix_map[Y_COUNT-y][x][5] = '-'

        self.coin_coord_abs = Coord(x,y)
        return self.coin_coord_abs

    def Agent_rand(self, isRand=False):
        if isRand == False:
            x = 3
            y = 4
            dir_abs = '∨'
        else:
            x, y = randint(1, 5), randint(1, 4)
            dir_abs = random.choice(['∧', '∨', '<', '>'])

        
        while self.matrix_map[Y_COUNT-y][x][4] == 'W' or self.matrix_map[Y_COUNT-y][x][4] == 'O' or self.matrix_map[Y_COUNT-y][x][4] == 'U':
            x, y = randint(1, 5), randint(1, 4)
            continue

        # update the current cell symbol 5 to dir
        self.matrix_map[Y_COUNT-y][x][4] = dir_abs
        # update the other cell sumbol 4/6 to space ' '
        xy_list_exclude_agent = set()
        xy_list_exclude_agent.add((x,y))
        map_helper.update_other_coord_in_matrix(self.matrix_map, ' ', 3, xy_list_exclude_agent)
        map_helper.update_other_coord_in_matrix(self.matrix_map, ' ', 5, xy_list_exclude_agent)

        # update the current cell symbol 1 to %
        self.matrix_map[Y_COUNT-y][x][0] = '%'
        # update the other cell sumbol 1 to .
        xy_list_exclude_confounded = set()
        xy_list_exclude_confounded.add((x,y))
        map_helper.update_other_coord_in_matrix(self.matrix_map, '.', 0, xy_list_exclude_confounded)

        # update the current cell symbol 4/6 to -
        self.matrix_map[Y_COUNT-y][x][3] = '-'
        self.matrix_map[Y_COUNT-y][x][5] = '-'

        self.agent = Agent(Coord(x,y), map_helper.dir_bi_translation(dir_abs), Coord(0,0), Direction.NORTH, 
                      [Sensory.CONFOUNDED_ON,Sensory.STENCH_OFF,Sensory.TINGLE_OFF,
                       Sensory.GLITTER_OFF,Sensory.BUMP_OFF,Sensory.SCREAM_OFF], True)
        
        self.agent.sensorylist = map_helper.convert_cell_to_sensory_list(self.matrix_map[self.agent.y_abs][self.agent.x_abs])

        # init agent in relative map
        self.matrix_map_rel[self.agent.y_rel_temp][self.agent.x_rel_temp][0] = '%'
        self.matrix_map_rel[self.agent.y_rel_temp][self.agent.x_rel_temp][3] = '-'
        self.matrix_map_rel[self.agent.y_rel_temp][self.agent.x_rel_temp][4] = map_helper.dir_bi_translation(self.agent.dir_rel)
        self.matrix_map_rel[self.agent.y_rel_temp][self.agent.x_rel_temp][5] = '-'


        return self.agent

    def Bump_trigger(self, agent_x, agent_y):
        self.matrix_map[Y_COUNT-agent_y][agent_x][7] = 'B'

    def Scream_trigger(self,agent_x, agent_y):
        self.matrix_map[Y_COUNT-agent_y][agent_x][8] = '@'

    

    
