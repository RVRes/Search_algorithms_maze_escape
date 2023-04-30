import os
from typing import List, Tuple, Optional
from tkinter import filedialog
from config import GridSymbols
from search_path import find_path


class Maze:
    def __init__(self, width: int, height: int):
        self.__agent_coords: Optional[Tuple[int, int]] = None
        self.__destination_coords: Optional[Tuple[int, int]] = None
        self.width: int = width
        self.height: int = height
        self.grid: List[List[int]] = [[0 for _ in range(self.width)] for _ in range(self.height)]  # maze 2D array

    def clear(self):
        """Clear the maze"""
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.__agent_coords = None
        self.__destination_coords = None

    def solve(self, search_algorythm: str):
        return find_path(self.grid, search_algorythm)

    def save(self):
        """Save the maze to a file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for row in self.grid:
                    for cell in row:
                        file.write(str(cell))
                    file.write("\n")

    def load(self):
        """load the maze from a file"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path and os.path.exists(file_path):
            with open(file_path, "r") as file:
                for y, line in enumerate(file):
                    for x, char in enumerate(line.strip()):
                        if y < self.height and x < self.width:
                            char = int(char)
                            self.grid[y][x] = char
                            if char == GridSymbols.START.value:
                                self.set_agent_coords(x, y)
                            elif char == GridSymbols.DESTINATION.value:
                                self.set_destination_coords(x, y)

    def __set_grid_value(self, x: int, y: int, item: int):
        if all((x >= 0, x < self.width, y >= 0, y < self.height)):
            self.grid[y][x] = item

    def set_wall(self, x: int, y: int) -> None:
        self.__set_grid_value(x, y, GridSymbols.WALL.value)

    # def set_explored(self, x: int, y: int) -> None:
    #     self.__set_grid_value(x, y, GridSymbols.EXPLORED.value)
    #
    # def set_path_found(self, x: int, y: int) -> None:
    #     self.__set_grid_value(x, y, GridSymbols.PATH.value)

    def clear_cell(self, x: int, y: int) -> None:
        if (x, y) == self.get_agent_coords():
            self.__agent_coords = None
        elif (x, y) == self.get_destination_coords():
            self.__destination_coords = None
        self.__set_grid_value(x, y, GridSymbols.EMPTY.value)

    def clear_explored(self) -> None:
        wiping_items = (GridSymbols.EXPLORED.value, GridSymbols.PATH.value)
        self.grid = [[0 if char in wiping_items else char for char in line] for line in self.grid]

    def set_agent_coords(self, x: int, y: int) -> None:
        if self.grid[y][x] != GridSymbols.WALL.value and self.__destination_coords != (x, y):
            if self.get_agent_coords():
                self.clear_cell(*self.get_agent_coords())
            self.__agent_coords = x, y
            self.__set_grid_value(x, y, GridSymbols.START.value)

    def get_agent_coords(self) -> Optional[Tuple[int, int]]:
        return self.__agent_coords

    def set_destination_coords(self, x: int, y: int) -> None:
        if self.grid[y][x] != GridSymbols.WALL.value and self.__agent_coords != (x, y):
            if self.get_destination_coords():
                self.clear_cell(*self.get_destination_coords())
            self.__destination_coords = x, y
            self.__set_grid_value(x, y, GridSymbols.DESTINATION.value)

    def get_destination_coords(self) -> Optional[Tuple[int, int]]:
        return self.__destination_coords
