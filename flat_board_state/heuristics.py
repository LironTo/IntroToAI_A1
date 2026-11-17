
def get_locations(_flat_board_state):
    board = _flat_board_state.get_state_board()

    cubes_locations = []
    holes_locations = []

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 3:
                cubes_locations.append((row, col))
            elif board[row][col] == 0:
                holes_locations.append((row, col))

    return cubes_locations, holes_locations


def manhattan_distance(position1, position2):
    return (
        abs(position1[0] - position2[0]) +
        abs(position1[1] - position2[1])
    )


def find_closest_cube_to_hole(cube_locations, hole_location):
    min_distance = float('inf')

    for cube in cube_locations:
        distance = manhattan_distance(cube, hole_location)
        min_distance = min(min_distance, distance)

    return min_distance


def base_heuristic(_flat_board_state):
    cubes, holes = get_locations(_flat_board_state)

    if not holes:
        return 0

    distances = []

    for hole in holes:
        distance = find_closest_cube_to_hole(cubes, hole)
        distances.append(distance)

    return max(distances)


def can_match_with_max_distance(cubes, holes, max_distance):
    n = len(cubes)
    matched_hole = [-1] * n

    def try_match(cube_index, visited):
        for hole_index in range(n):

            if visited[hole_index]:
                continue

            distance = manhattan_distance(
                cubes[cube_index],
                holes[hole_index]
            )

            if distance > max_distance:
                continue

            visited[hole_index] = True

            if (matched_hole[hole_index] == -1 or
                    try_match(matched_hole[hole_index], visited)):

                matched_hole[hole_index] = cube_index
                return True

        return False

    for cube_index in range(n):
        visited = [False] * n

        if not try_match(cube_index, visited):
            return False

    return True


def find_min_bottleneck_matching(cubes, holes):
    if not cubes or not holes:
        return 0

    if len(cubes) != len(holes):
        return 0

    distances = sorted({
        manhattan_distance(cube, hole)
        for cube in cubes
        for hole in holes
    })

    left = 0
    right = len(distances) - 1

    while left < right:
        mid = (left + right) // 2

        if can_match_with_max_distance(
            cubes,
            holes,
            distances[mid]
        ):
            right = mid
        else:
            left = mid + 1

    return distances[left]


# Every move pushes all cubes the same way, so the moves toward the two sides of one axis add up:
# if one cube must go 3 left and another 3 right, at least 6 moves are needed.
# Matching the sorted lists gives the fewest moves needed toward each side.
def axis_moves(cube_values, hole_values):
    pairs = list(zip(sorted(cube_values), sorted(hole_values)))
    backward = max(cube - hole for cube, hole in pairs)
    forward = max(hole - cube for cube, hole in pairs)
    return max(0, backward) + max(0, forward)


def advanced_heuristic(_flat_board_state):
    cubes, holes = get_locations(_flat_board_state)

    if not holes:
        return 0

    return find_min_bottleneck_matching(cubes, holes)
