# you can add global params
# Cell states:
HOLE = 0
CELL = 1
WALL = 2
CUBE = 3

# Move directions:
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class flat_board_state:
    def __init__(self, instance_map=None, *args, **kwargs):
        self.instance_map = instance_map
        self._hash = None

    @staticmethod
    def is_goal_state(_flat_board_state):
        for i in range(len(_flat_board_state.instance_map)):
            for j in range(len(_flat_board_state.instance_map[0])):
                if _flat_board_state.instance_map[i][j] == CUBE or _flat_board_state.instance_map[i][j] == HOLE:
                    return False
        return True
    

    def get_neighbors(self):
        neighbors = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            new_state = flat_board_state(self.move(direction))
            if new_state != self:
                neighbors.append((new_state, 1))
        return neighbors


    # you can change the body of the function if you want
    def __hash__(self):
        # the search hashes the same state many times (OPEN/CLOSED lookups), so compute it only once
        if self._hash is None:
            self._hash = hash(tuple(map(tuple, self.instance_map)))
        return self._hash

    # you can change the body of the function if you want
    def __eq__(self, other):
        if not isinstance(other, flat_board_state):
            return False
        return self.instance_map == other.instance_map

    def get_state_board(self):
        return self.instance_map

    def get_state_str(self):
        return str(self.instance_map)

    # you can add helper functions

    def move(self, direction):
        # direction is (dx, dy) with y pointing up (UP = (0, 1)),
        # but in the board row 0 is the top row, so the row step is -dy.
        dx, dy = direction
        dr, dc = -dy, dx
    
        board = [row[:] for row in self.instance_map]  # copy, so the current state is not changed
        rows = len(board)
        cols = len(board[0])
    
        # Go over the cubes starting from the side they move toward,
        # so a cube in front moves (or gets stuck) before the cube behind it.
        row_order = range(rows - 1, -1, -1) if dr == 1 else range(rows)
        col_order = range(cols - 1, -1, -1) if dc == 1 else range(cols)
    
        for r in row_order:
            if CUBE not in board[r]:  # quick skip of rows without cubes
                continue
            for c in col_order:
                if board[r][c] != CUBE:
                    continue
                nr, nc = r + dr, c + dc
                if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                    continue  # board edge acts as a wall
                if board[nr][nc] == CELL:  # free cell: slide into it
                    board[nr][nc] = CUBE
                    board[r][c] = CELL
                elif board[nr][nc] == HOLE:  # hole: cube fills it and disappears
                    board[nr][nc] = CELL
                    board[r][c] = CELL
                # WALL or a stuck CUBE: stay in place
        return board
    