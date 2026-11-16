
import time

from search import search, get_gen_exp_count
from heuristics import *
from flat_board_state import *


if __name__ == '__main__':

    board = board = [
    [3, 0, 1, 3],
    [0, 1, 1, 1]
]

    start_state = flat_board_state(board)

    # Test both heuristics
    heuristics = [
        ("Base", base_heuristic),
        ("Advanced", advanced_heuristic)
    ]

    for name, heuristic in heuristics:

        print("\n" + "=" * 40)
        print(f"Testing {name} Heuristic")
        print("=" * 40)

        # Print heuristic value for initial state
        h = heuristic(start_state)
        print("Initial heuristic value:", h)

        # Run A*
        start_time = time.perf_counter()
        search_result = search(start_state, heuristic)
        runtime = time.perf_counter() - start_time

        generated, expanded = get_gen_exp_count()

        print("Runtime:", runtime)
        print("Solution cost:", search_result[-1].g)
        print("Generated:", generated)
        print("Expanded:", expanded)
