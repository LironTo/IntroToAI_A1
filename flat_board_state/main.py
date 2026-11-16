import time

from search import search, get_gen_exp_count
from heuristics import *
from flat_board_state import *


if __name__ == '__main__':

    board = [[3, 3, 0], [2, 2, 1], [0, 1, 1]]

    start_state = flat_board_state(board)

    # Test base heuristic
    print("\nTesting base heuristic:")
    h = base_heuristic(start_state, debug=True)
    print("Returned heuristic:", h)

    # Run A*
    print("\nStarting A* search:")

    start_time = time.time()
    search_result = search(start_state, base_heuristic)
    end_time = time.time() - start_time

    print("Runtime:", end_time)
    print("Solution cost:", search_result[-1].g)
    print("Generated / Expanded:", get_gen_exp_count())