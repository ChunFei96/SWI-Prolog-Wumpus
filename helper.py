from statistics import NormalDist
from coord import Coord
from constant import Direction, Sensory, Action
from prettytable import PrettyTable

class map_helper:
    def is_coord_in_matrix(matrix, x, y):
        # -2 to exclude wall cells
        return y >=1 and y <= len(matrix) - 2 and x >=1 and x <= len(matrix[y]) - 2

    def update_other_coord_in_matrix(matrix, update_symbol, update_location, xy_list_exclude):

        if len(xy_list_exclude) <=0:
            return False
        
        for x in range(1,6):
            for y in range(1,5):
                if (x,y) not in xy_list_exclude and matrix[y][x][update_location] == update_location+1:
                    matrix[y][x][update_location] = update_symbol

    def dir_bi_translation(dir):
        if dir == '∧':
            return Direction.NORTH
        elif dir == '∨':
            return Direction.SOUTH
        elif dir == '<':
            return Direction.WEST
        elif dir == '>':
            return Direction.EAST
        elif dir == Direction.NORTH:
            return '∧'
        elif dir == Direction.SOUTH:
            return '∨'
        elif dir == Direction.WEST:
            return '<'
        elif dir == Direction.EAST:
            return '>'
    
    def find_safe_cell(matrix):
        for x in range(1,6):
            for y in range(1,5):
                if matrix[y][x][4] != 'W' and matrix[y][x][4] != 'O':
                    return Coord(x,y)

    def convert_cell_to_sensory_list(cell):
        sensorylist = [Sensory.CONFOUNDED_OFF,Sensory.STENCH_OFF,Sensory.TINGLE_OFF,
                       Sensory.GLITTER_OFF,Sensory.BUMP_OFF,Sensory.SCREAM_OFF]

        if cell[0] == '%':
            sensorylist[0] = Sensory.CONFOUNDED_ON
        if cell[1] == '=':
            sensorylist[1] = Sensory.STENCH_ON
        if cell[2] == 'T':
            sensorylist[2] = Sensory.TINGLE_ON
        if cell[6] == '*':
            sensorylist[3] = Sensory.GLITTER_ON
        
        return sensorylist

    def update_agent_dir_in_map(matrix_map, agent):
        matrix_map[agent.y_abs][agent.x_abs][4] = map_helper.dir_bi_translation(agent.dir_abs)

        # update agent sensory list BUMP to OFF in case previous MOVEFORWARD bump into a wall
        # since changing direction will never bump into a wall, so it is safe to always set BUMP to OFF
        agent.sensorylist[4] = Sensory.BUMP_OFF
    
    def update_agent_loc_in_map(matrix_map, agent):
        #TODO call reborn when stepping into Wumpus cell
        #TODO call reposition when stepping into Confoundus portal cell
        if agent.dir_abs == Direction.NORTH:
            
            # check if the new location is a wall 
            if matrix_map[agent.y_abs - 1][agent.x_abs][4] == '#':
                # update agent sensory list BUMP to ON
                agent.sensorylist[4] = Sensory.BUMP_ON

                # stay in the original cell
            else:
                # update the old location symbol 1 to '.'
                matrix_map[agent.y_abs][agent.x_abs][0] = '.'

                # update the old location symbol 5 to 'S' (safe cell visited)
                matrix_map[agent.y_abs][agent.x_abs][3] = ' '
                matrix_map[agent.y_abs][agent.x_abs][4] = 'S'
                matrix_map[agent.y_abs][agent.x_abs][5] = ' '

                agent.y_abs += 1
                agent.y_rel += 1
                
                # update the new location symbol 5 to agent direction
                matrix_map[agent.y_abs][agent.x_abs][3] = '-'
                matrix_map[agent.y_abs][agent.x_abs][4] = map_helper.dir_bi_translation(agent.dir_abs)
                matrix_map[agent.y_abs][agent.x_abs][5] = '-'

                # update the agent sensory list with new location cell
                agent.sensorylist = map_helper.convert_cell_to_sensory_list(matrix_map[agent.y_abs][agent.x_abs])

                # update agent sensory list BUMP to OFF
                agent.sensorylist[4] = Sensory.BUMP_OFF
            
        elif agent.dir_abs == Direction.SOUTH:
            
            # check if the new location is a wall 
            if matrix_map[agent.y_abs + 1][agent.x_abs][4] == '#':
                # update agent sensory list BUMP to ON
                agent.sensorylist[4] = Sensory.BUMP_ON

                # stay in the original cell
            else:
                # update the old location symbol 1 to '.'
                matrix_map[agent.y_abs][agent.x_abs][0] = '.'

                # update the old location symbol 5 to 'S' (safe cell visited)
                matrix_map[agent.y_abs][agent.x_abs][3] = ' '
                matrix_map[agent.y_abs][agent.x_abs][4] = 'S'
                matrix_map[agent.y_abs][agent.x_abs][5] = ' '

                agent.y_abs -= 1
                agent.y_rel -= 1

                # update the new location symbol 5 to agent direction
                matrix_map[agent.y_abs][agent.x_abs][3] = '-'
                matrix_map[agent.y_abs][agent.x_abs][4] = map_helper.dir_bi_translation(agent.dir_abs)
                matrix_map[agent.y_abs][agent.x_abs][5] = '-'

                # update the agent sensory list with new location cell
                agent.sensorylist = map_helper.convert_cell_to_sensory_list(matrix_map[agent.y_abs][agent.x_abs])

                # update agent sensory list BUMP to OFF
                agent.sensorylist[4] = Sensory.BUMP_OFF
            
        elif agent.dir_abs == Direction.WEST:
            
            # check if the new location is a wall 
            if matrix_map[agent.y_abs][agent.x_abs-1][4] == '#':
                # update agent sensory list BUMP to ON
                agent.sensorylist[4] = Sensory.BUMP_ON

                # stay in the original cell
            else:
                # update the old location symbol 1 to '.'
                matrix_map[agent.y_abs][agent.x_abs][0] = '.'

                # update the old location symbol 5 to 'S' (safe cell visited)
                matrix_map[agent.y_abs][agent.x_abs][3] = ' '
                matrix_map[agent.y_abs][agent.x_abs][4] = 'S'
                matrix_map[agent.y_abs][agent.x_abs][5] = ' '

                agent.x_abs -= 1
                agent.x_rel -= 1

                # update the new location symbol 5 to agent direction
                matrix_map[agent.y_abs][agent.x_abs][3] = '-'
                matrix_map[agent.y_abs][agent.x_abs][4] = map_helper.dir_bi_translation(agent.dir_abs)
                matrix_map[agent.y_abs][agent.x_abs][5] = '-'

                # update the agent sensory list with new location cell
                agent.sensorylist = map_helper.convert_cell_to_sensory_list(matrix_map[agent.y_abs][agent.x_abs])

                # update agent sensory list BUMP to OFF
                agent.sensorylist[4] = Sensory.BUMP_OFF

        elif agent.dir_abs == Direction.EAST:
            
            if matrix_map[agent.y_abs][agent.x_abs+1][4] == '#':
                # update agent sensory list BUMP to ON
                agent.sensorylist[4] = Sensory.BUMP_ON

                # stay in the original cell
            else:
                # update the old location symbol 1 to '.'
                matrix_map[agent.y_abs][agent.x_abs][0] = '.'

                # update the old location symbol 5 to 'S' (safe cell visited)
                matrix_map[agent.y_abs][agent.x_abs][3] = ' '
                matrix_map[agent.y_abs][agent.x_abs][4] = 'S'
                matrix_map[agent.y_abs][agent.x_abs][5] = ' '

                agent.x_abs += 1
                agent.x_rel += 1

                # update the new location symbol 5 to agent direction
                matrix_map[agent.y_abs][agent.x_abs][3] = '-'
                matrix_map[agent.y_abs][agent.x_abs][4] = map_helper.dir_bi_translation(agent.dir_abs)
                matrix_map[agent.y_abs][agent.x_abs][5] = '-'

                # update the agent sensory list with new location cell
                agent.sensorylist = map_helper.convert_cell_to_sensory_list(matrix_map[agent.y_abs][agent.x_abs])

                # update agent sensory list BUMP to OFF
                agent.sensorylist[4] = Sensory.BUMP_OFF


    def update_wumpus_in_map(matrix_map, agent):
        if agent.dir_abs == Direction.NORTH:
            y = agent.y_abs - 1

            # if forward cell is not wall, keep the arrow travelling
            while matrix_map[y][agent.x_abs][4] != '#':
                if matrix_map[y][agent.x_abs][4] == 'W':
                    # kill wumpus by update the symbol 5 to '?'
                    matrix_map[y][agent.x_abs][4] = '?'

                    # update agent's sensory list SCREAM to ON
                    agent.sensorylist[5] = Sensory.SCREAM_ON

                    # update agent's hasarrow to false
                    agent.hasarrow = False
                    break
                else:
                    y -= 1

        elif agent.dir_abs == Direction.SOUTH:
            y = agent.y_abs + 1

            # if forward cell is not wall, keep the arrow travelling
            while matrix_map[y][agent.x_abs][4] != '#':
                if matrix_map[y][agent.x_abs][4] == 'W':
                    # kill wumpus by update the symbol 5 to '?'
                    matrix_map[y][agent.x_abs][4] = '?'

                    # update agent's sensory list SCREAM to ON
                    agent.sensorylist[5] = Sensory.SCREAM_ON

                    # update agent's hasarrow to false
                    agent.hasarrow = False

                    break
                else:
                    y += 1

        elif agent.dir_abs == Direction.WEST:
            x = agent.y_abs - 1

            # if forward cell is not wall, keep the arrow travelling
            while matrix_map[agent.y_abs][x][4] != '#':
                if matrix_map[agent.y_abs][x][4] == 'W':
                    # kill wumpus by update the symbol 5 to '?'
                    matrix_map[agent.y_abs][x][4] = '?'

                    # update agent's sensory list SCREAM to ON
                    agent.sensorylist[5] = Sensory.SCREAM_ON

                    # update agent's hasarrow to false
                    agent.hasarrow = False

                    break
                else:
                    x -= 1

        elif agent.dir_abs == Direction.EAST:
            x = agent.y_abs + 1

            # if forward cell is not wall, keep the arrow travelling
            while matrix_map[agent.y_abs][x][4] != '#':
                if matrix_map[agent.y_abs][x][4] == 'W':
                    # kill wumpus by update the symbol 5 to '?'
                    matrix_map[agent.y_abs][x][4] = '?'

                    # update agent's sensory list SCREAM to ON
                    agent.sensorylist[5] = Sensory.SCREAM_ON

                    # update agent's hasarrow to false
                    agent.hasarrow = False

                    break
                else:
                    x += 1


    def update_coin_in_map(matrix_map, agent):
        if matrix_map[agent.y_abs][agent.x_abs][6] == '*':
            matrix_map[agent.y_abs][agent.x_abs][6] = '.'
            agent.sensorylist[3] = Sensory.GLITTER_OFF

    def draw_map(matrix_map, r_cell, c_cell):
        print('======================================================================================================================')
        print("Absolute map")
        for row in matrix_map[::-1]:
            char_pointer = 0
            while char_pointer != r_cell * c_cell :
                for cell in row:
                    for i in range(char_pointer, char_pointer+3, 1):
                        if i != char_pointer+2:
                            print(cell[i], end=' ')
                        else:
                            print(cell[i], end='   ')
                print()    
                char_pointer += 3
            print()
        
        print('======================================================================================================================')

    def draw_npc_table(map_ref):
        table = PrettyTable(['NPC', 'Absolute position'])
        table.add_row(['Agent', (map_ref.agent.x_abs, map_ref.agent.y_abs, map_ref.agent.dir_abs)])
        table.add_row(['Wumpus', (map_ref.wumpus_coord_abs.x , map_ref.wumpus_coord_abs.y)])
        table.add_row(['Portal 1', (map_ref.portal_coord_abs_list[0].x , map_ref.portal_coord_abs_list[0].y)])
        table.add_row(['Portal 2', (map_ref.portal_coord_abs_list[1].x , map_ref.portal_coord_abs_list[1].y)])
        table.add_row(['Portal 3', (map_ref.portal_coord_abs_list[2].x , map_ref.portal_coord_abs_list[2].y)])
        table.add_row(['Coin', (map_ref.coin_coord_abs.x , map_ref.coin_coord_abs.y)])
        print(table)

    def draw_agent_table(action, map_ref):
        table_agent = PrettyTable(['Attribute', 'Value'])
        table_agent.add_row(['Action', action])
        table_agent.add_row(['Sensory Input', map_ref.agent.sensorylist])
        table_agent.add_row(['Absolute position', (map_ref.agent.x_abs, map_ref.agent.y_abs, map_ref.agent.dir_abs)])
        table_agent.add_row(['Relative position', (map_ref.agent.x_rel, map_ref.agent.y_rel, map_ref.agent.dir_rel)])
        print(table_agent)

class agent_helper:
    def change_agent_direction(agent_dir, action):
        if action == Action.TURNLEFT:
            if agent_dir == Direction.NORTH:
                return Direction.WEST
            elif agent_dir == Direction.WEST:
                return Direction.SOUTH
            elif agent_dir == Direction.SOUTH:
                return Direction.EAST
            elif agent_dir == Direction.EAST:
                return Direction.NORTH
                
        elif action == Action.TURNRIGHT:
            if agent_dir == Direction.NORTH:
                return Direction.EAST
            elif agent_dir == Direction.EAST:
                return Direction.SOUTH
            elif agent_dir == Direction.SOUTH:
                return Direction.WEST
            elif agent_dir == Direction.WEST:
                return Direction.NORTH




