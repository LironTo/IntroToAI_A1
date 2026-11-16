
def find_closest_cube_to_hole(cube_locations, hole_location):
    min_distance = float('inf')

    for cube in cube_locations:
        distance = abs(cube[0] - hole_location[0]) + abs(cube[1] - hole_location[1])

        min_distance = min(min_distance, distance)

    return min_distance


def base_heuristic(_flat_board_state, debug=False):
    board = _flat_board_state.get_state_board()

    cubes_locations = []
    holes_locations = []

    # Find all cubes and holes on the board
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 3:
                cubes_locations.append((row, col))
            elif board[row][col] == 0:
                holes_locations.append((row, col))

    if not holes_locations:
        return 0

    distances = []

    # Find the closest cube for each hole
    for hole in holes_locations:
        distance = find_closest_cube_to_hole(cubes_locations, hole)
        distances.append(distance)

    result = max(distances)

    # Debugging prints
    if debug:
        print("\n========== BASE HEURISTIC DEBUG ==========")
        print("Board:")
        for row in board:
            print(row)

        print("\nCube locations:", cubes_locations)
        print("Hole locations:", holes_locations)

        print("\nDistances:")
        for hole, distance in zip(holes_locations, distances):
            print(f"Hole {hole}: closest cube distance = {distance}")

        print("\nAll distances:", distances)
        print("Heuristic value:", result)
        print("==========================================\n")

    return result


def advanced_heuristic(_flat_board_state):
    return 0
