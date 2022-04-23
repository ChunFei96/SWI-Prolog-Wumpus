from asyncio.windows_events import NULL
from helper import map_helper
from map import map
from constant import *
from prettytable import PrettyTable
from prolog_command import prolog_command

ROW_MAP = 7
COL_MAP = 6
ROW_CELL = 3
COL_CELL = 3

def main():
    map_ref = map(ROW_MAP,COL_MAP,ROW_CELL,COL_CELL)
    map_ref.map_generator()

    # init npc table
    map_helper.draw_npc_table(map_ref)
     # draw absolute map
    map_helper.draw_map(map_ref.matrix_map, ROW_CELL, COL_CELL)

    driver = prolog_command(map_ref)
    driver.correctness_of_localisation_mapping()


if __name__ == "__main__":
    main()
