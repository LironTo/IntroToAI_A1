import heapq
import itertools

from search_node import search_node
from flat_board_state import flat_board_state

count_generated = 0
count_expanded = 0

# OPEN is [heap, nodes, counter]:
#   heap    - heap of (f, h, counter, node); same order as search_node.__lt__ (lowest f, then lowest h),
#             but comparing tuples of numbers is much faster than calling __lt__.
#             counter breaks the remaining ties, so two nodes are never compared directly.
#   nodes   - dict state -> node, for fast duplicate checks
# A node removed from OPEN is only deleted from the dict; get_best skips it when it reaches the top of the heap.
def create_open_set():
    return [[], {}, itertools.count()]


# CLOSED is a dict state -> node
def create_closed_set():
    return {}


def add_to_open(vn, open_set):
    heap, nodes, counter = open_set
    heapq.heappush(heap, (vn.f, vn.h, next(counter), vn))
    nodes[vn.state] = vn


def open_not_empty(open_set):
    nodes = open_set[1]
    return len(nodes) > 0


def get_best(open_set):
    heap, nodes, _ = open_set
    while True:
        node = heapq.heappop(heap)[3]
        if nodes.get(node.state) is node:  # skip nodes that were removed from OPEN
            del nodes[node.state]
            return node


def add_to_closed(vn, closed_set):
    closed_set[vn.state] = vn

#returns False if curr_neighbor state not in open_set or has a lower g from the node in open_set
#remove the node with the higher g from open_set (if exists)
def duplicate_in_open(vn, open_set):
    nodes = open_set[1]
    old = nodes.get(vn.state)
    if old is None:
        return False
    if old.g <= vn.g:
        return True
    del nodes[vn.state]  # the new node is better; the old one stays in the heap and is skipped later
    return False

#returns False if curr_neighbor state not in closed_set or has a lower g from the node in closed_set
#remove the node with the higher g from closed_set (if exists)
def duplicate_in_closed(vn, closed_set):
    old = closed_set.get(vn.state)
    if old is None:
        return False
    if old.g <= vn.g:
        return True
    del closed_set[vn.state]
    return False


# helps to debug sometimes..
def print_path(path):
    for i in range(len(path)-1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.state_str)

def get_gen_exp_count():
    global count_generated
    global count_expanded
    return count_generated, count_expanded

def search(start_state, heuristic):
    global count_generated
    global count_expanded
    count_generated = 0
    count_expanded = 0
    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):

        current = get_best(open_set)

        if flat_board_state.is_goal_state(current.state):
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)
        count_expanded += 1

        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_open(curr_neighbor, open_set) and not duplicate_in_closed(curr_neighbor, closed_set):
                add_to_open(curr_neighbor, open_set)
                count_generated += 1

    return None




