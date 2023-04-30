from collections import namedtuple
from typing import Optional, List

Coords = namedtuple('Coords', ['width', 'height'])


class Node:
    """Node class that stores coordinates of the cell, link to parent Node
    and rating for Greedy BFS and A* algorithms."""

    def __init__(self, coords: Coords, parent, rating: Optional[int] = None):
        self.parent = parent
        self.rating = rating
        self.coords = coords


def __get_possible_moves(maze_: list, current_node: Node) -> list:
    """Finds free cells (0 - valued) that surrounds current cell and returns list of possible moves."""
    coords = current_node.coords
    neighbours = ((0, 1), (1, 0), (0, -1), (-1, 0))
    possible_moves = []
    for neighbour in neighbours:
        neighbour_coords = Coords(coords.width + neighbour[0], coords.height + neighbour[1])
        if (0 <= neighbour_coords.width < len(maze_[coords.height]) and 0 <= neighbour_coords.height < len(maze_)
                and (maze_[neighbour_coords.height][neighbour_coords.width] == 0
                     or maze_[neighbour_coords.height][neighbour_coords.width] == 5)):
            possible_moves.append(Node(neighbour_coords, current_node))
    return possible_moves


def __get_pos_by_value(maze: list, value: int) -> Optional[Coords]:
    """Returns 1st occurrence Coord in maze by value or None if not found."""
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == value:
                return Coords(x, y)
    return None


def __calculate_greedy_bfs_rating(current: Node, finish: Node) -> int:
    """Calculates rating for given position for greedy BFS search. Counts manhattan distance to finish."""
    dx = abs(finish.coords.width - current.coords.width)
    dy = abs(finish.coords.height - current.coords.height)
    return dx + dy


def __calculate_a_star_rating(current: Node, finish: Node) -> int:
    """Calculates rating for given position for greedy BFS search. Counts both
    manhattan distance to finish and walked path."""
    rating = __calculate_greedy_bfs_rating(current, finish)
    moved_path = 1
    parent_node = current
    while parent_node is not None:
        moved_path += 1
        parent_node = parent_node.parent
    return rating + moved_path


def find_path(maze: List[List[int]], selected_mode: str) -> (List[Node], List[Node]):
    """
    Finds path from start to finish. Returns list of moves and found path. Different search algorythm can be used by
    setting up selected mode argument.
    :param maze: maze grid of integers.
                (0 - free space, 1 - wall, 2 - explored cells, 3 - found path, 4 - start, 5 - destination)
    :param selected_mode: Selects search algorythm:
                ('BFS' - uninformed. finds optimal solution,
                 'DFS' - uninformed,
                 'Greedy BFS' - informed. Heuristics rating based on the destination to target,
                 'A*' - informed. Heuristics rating based on the destination to target and walked path,
                        finds optimal solution.)
    :return: List of inspected cells before the path is found, list of cells for found path or [].
    """
    stack, path, moves = [], [], []
    start_node = Node(__get_pos_by_value(maze, 4), None)  # find start coords in maze (cell value = 4)
    destination_node = Node(__get_pos_by_value(maze, 5), None)  # find finish coords in maze (cell value = 5)
    node = start_node
    while True:
        possible_moves = __get_possible_moves(maze, node)
        if destination_node.coords in (possible_move.coords for possible_move in possible_moves):
            while node.coords != start_node.coords:
                path.append(node)
                node = node.parent
            return moves, path
        possible_moves = list(filter(lambda x: x.coords not in (m.coords for m in stack + moves), possible_moves))
        if selected_mode in ['Greedy BFS', 'A*']:
            for possible_move in possible_moves:
                possible_move.rating = __calculate_greedy_bfs_rating(possible_move, destination_node) \
                    if selected_mode == 'Greedy BFS' else __calculate_a_star_rating(possible_move, destination_node)
        stack.extend(possible_moves)
        if not stack:
            return moves, []
        if selected_mode == 'BFS':
            node = stack.pop(0)
        elif selected_mode == 'DFS':
            node = stack.pop(-1)
        elif selected_mode in ['Greedy BFS', 'A*']:
            stack.sort(key=lambda x: x.rating)
            node = stack.pop(0)
        moves.append(node)


def find_path_select_mode(maze_: list) -> list:
    """Search mode selector for path finding function. Adds search mode selected by user to main function execution."""
    search_modes = ('BFS', 'DFS', 'Greedy BFS', 'A*')
    users_answer = int(input(f'Input path search mode: ' +
                             "".join((f"{pos + 1}. {mode}, " for pos, mode in enumerate(search_modes)))[:-2] + ': '))
    return find_path(maze_, search_modes[users_answer - 1])
