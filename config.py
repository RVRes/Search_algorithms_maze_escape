from collections import namedtuple
from enum import Enum


class Colors:
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GREEN_EAGLE = (0, 73, 83)
    RED = (255, 0, 0)
    CREAM = (253, 244, 227)
    AZURE_BLUE = (2, 86, 105)
    AZURE = (0, 127, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 136, 0)
    ORANGE_LITE = (255, 210, 0)
    FUCHSIA = (255, 0, 255)


class __NextEnumMixin:
    """Mixin for Enum objects that allows to get next element in Enum object."""
    def next(self):
        members = list(self.__class__)
        index = (members.index(self) + 1) % len(members)
        return members[index]


class GridSymbols(Enum):
    EMPTY = 0
    WALL = 1
    EXPLORED = 2
    PATH = 3
    START = 4
    DESTINATION = 5


class SceneDrawingModes(__NextEnumMixin, Enum):
    WALLS = 1
    AGENT = 2
    DESTINATION = 3


class SearchAlgorithmModes(__NextEnumMixin, Enum):
    BFS = 'BFS'
    DFS = 'DFS'
    GREEDY_BFS = 'Greedy BFS'
    A_STAR = 'A*'


class Settings:
    # Constants
    BACKGROUND_COLOR = Colors.CREAM
    WALL_COLOR = Colors.AZURE_BLUE
    AGENT_COLOR = Colors.AZURE
    DESTINATION_COLOR = Colors.RED
    EXPLORED_COLOR = Colors.ORANGE_LITE
    PATH_FOUND_COLOR = Colors.GREEN

    _Size = namedtuple('Size', ['width', 'height'])
    WINDOW_SIZE = _Size(width=800, height=850)

    GRID_SIZE = 20  # Set the size of the grid
    LABEL_HEIGHT = 50

    FPS = 60
