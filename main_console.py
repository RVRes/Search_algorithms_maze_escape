import os
import sys
from time import sleep
from typing import List

import search_path
from search_path import find_path_select_mode


class Color:
    """Console colors dataclass."""
    CIAN = '\033[1;36;48m'
    YELLOW = '\033[1;33;48m'
    GREEN = '\033[1;32;48m'
    RED = '\033[1;31;48m'
    BLUE = '\033[1;34;48m'
    PURPLE = '\033[1;35;48m'
    RESET = '\x1b[0m'


def load_maze(file_name: str) -> List[List[int]]:
    """load the maze from a file"""
    if not file_name or not os.path.exists(file_name):
        raise FileExistsError
    with open(file_name, "r") as file:
        return [[int(char) for char in line.strip()] for line in file]


def draw_maze_numbers(maze_: List[List[int]]) -> None:
    """Draw maze numbers."""
    os.system('cls||clear')
    for line in maze_:
        print(*line)


def draw_maze(maze_: List[List[int]]) -> None:
    """Draw maze in console using colors and special symbols."""
    wall, path, start = '■', '◆', '●'
    cell_styles = {
        0: ' ',  # free cell
        1: Color.BLUE + wall + Color.RESET,  # wall
        2: Color.YELLOW + path + Color.RESET,  # explored cells
        3: Color.PURPLE + path + Color.RESET,  # found path
        4: Color.GREEN + start + Color.RESET,  # start
        5: Color.RED + start + Color.RESET  # finish / destination
    }
    os.system('cls||clear')
    for line in maze_:
        print(*(cell_styles[char] for char in line))


def __fill_cells(maze_:  List[List[int]], cells_fill_list: List[search_path.Node], fill_value: int, delay: float):
    """
    Fills maze with fill_value for cells given in cells_fill_list. After single cell change redraws maze
    and wait for delay. Used to animate the search process and drawing of the found path.
    :param maze_: maze grid of integers.
                (0 - free space, 1 - wall, 2 - explored cells, 3 - found path, 4 - start, 5 - destination)
    :param cells_fill_list: List of Nodes to fill the maze.
    :param fill_value: Value to fill the maze.
    :param delay: delay in seconds before draw next cell. The best values are between 0.01 and 0.1
    """
    for cell in cells_fill_list:
        maze_[cell.coords.height][cell.coords.width] = fill_value
        draw_maze(maze_)
        sleep(delay)


def run(filename_: str) -> None:
    """Console application that allows to draw maze without using pygame. Loads maze from file.
    Asks to select search algorithm, solves the maze and animate the process of the search.
    Note: Pycharm console can't clear screen correctly, use standard Linux / Windows console."""
    maze = load_maze(filename_)
    draw_maze(maze)
    moves, path = find_path_select_mode(maze)
    __fill_cells(maze, moves, 2, 0.01)
    __fill_cells(maze, path, 3, 0.01)
    print(f'Explored cells: {len(moves)}, Path: {len(path)} cells.')


if __name__ == "__main__":
    """Reads console argument: maze filename. Opens maze.txt if empty."""
    filename = sys.argv[1] if len(sys.argv) > 1 else 'maze.txt'
    run(filename)
