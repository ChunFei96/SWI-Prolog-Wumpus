from pyswip import Prolog
from query import query
from constant import Action
from helper import map_helper

prolog = Prolog()
#prolog.consult("agent.pl")

class prolog_command:
    def __init__(self, map_ref) -> None:
        self.map_ref= map_ref

    def correctness_of_localisation_mapping(self):
        
        query_ref = query()

        # move forward
        query_ref.move(self.map_ref.matrix_map, self.map_ref.agent, Action.MOVEFORWARD)
        prolog.query("move(" + Action.MOVEFORWARD + "," + str(self.map_ref.agent.sensorylist) + ")")
        map_helper.draw_agent_table(Action.MOVEFORWARD, self.map_ref)
        #map_helper.draw_map_abs(self.map_ref.matrix_map, 3, 3)

        # move forward
        query_ref.move(self.map_ref.matrix_map, self.map_ref.agent, Action.MOVEFORWARD)
        prolog.query("move(" + Action.MOVEFORWARD + "," + str(self.map_ref.agent.sensorylist) + ")")
        map_helper.draw_agent_table(Action.MOVEFORWARD, self.map_ref)
        #map_helper.draw_map_abs(self.map_ref.matrix_map, 3, 3)
        
        # move turnleft
        query_ref.move(self.map_ref.matrix_map, self.map_ref.agent, Action.TURNLEFT)
        prolog.query("move(" + Action.TURNLEFT + "," + str(self.map_ref.agent.sensorylist) + ")")
        map_helper.draw_agent_table(Action.TURNLEFT, self.map_ref)
        #map_helper.draw_map_abs(self.map_ref.matrix_map, 3, 3)

        # move forward
        query_ref.move(self.map_ref.matrix_map, self.map_ref.agent, Action.MOVEFORWARD)
        prolog.query("move(" + Action.MOVEFORWARD + "," + str(self.map_ref.agent.sensorylist) + ")")
        map_helper.draw_agent_table(Action.MOVEFORWARD, self.map_ref)
        #map_helper.draw_map_abs(self.map_ref.matrix_map, 3, 3)

        # move turnright
        query_ref.move(self.map_ref.matrix_map, self.map_ref.agent, Action.TURNRIGHT)
        prolog.query("move(" + Action.TURNRIGHT + "," + str(self.map_ref.agent.sensorylist) + ")")
        map_helper.draw_agent_table(Action.TURNRIGHT, self.map_ref)
        #map_helper.draw_map_abs(self.map_ref.matrix_map, 3, 3)
        

    def correctness_of_sensory_inference():
        pass

    def correctness_of_memory_management_of_confundus_portal():
        pass

    def correctness_of_exploration_capabilities():
        pass

    def correctness_of_end_game_reset():
        pass
