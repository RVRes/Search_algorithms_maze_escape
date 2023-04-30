import pygame
from config import Colors, Settings, SceneDrawingModes, SearchAlgorithmModes, GridSymbols
from maze import Maze
from time import sleep


class Scene:
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.WINDOW_SIZE)  # Set the dimensions of the screen
        pygame.display.set_caption("Maze Editor")  # Set the title of the window
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 15)  # Load font for drawing text
        self.drawing_mode = SceneDrawingModes.WALLS
        self.search_algorythm = SearchAlgorithmModes.BFS  # Selected search algorythm
        self.erasing_mode = False  # Set erasing mode (right mouse button pressed)
        self.maze = Maze(*Scene.__get_grid_cords(*Settings.WINDOW_SIZE))
        self.mouse_pressed = False

    @staticmethod
    def __get_grid_cords(x: int, y: int):
        """Converts position in pixels to gird coordinates"""
        grid_x = x // Settings.GRID_SIZE
        grid_y = (y - Settings.LABEL_HEIGHT) // Settings.GRID_SIZE
        return grid_x, grid_y

    def __draw_grid_rect(self, x: int, y: int, color: tuple):
        """draw a rectangle at a given grid position"""
        pygame.draw.rect(self.screen, color, (x * Settings.GRID_SIZE + 1, y * Settings.GRID_SIZE + 50 + 1,
                                              Settings.GRID_SIZE - 1, Settings.GRID_SIZE - 1))

    def __draw_maze(self):
        """draw the maze"""
        cell_colors = {
            GridSymbols.EMPTY.value: Settings.BACKGROUND_COLOR,
            GridSymbols.WALL.value: Settings.WALL_COLOR,
            GridSymbols.EXPLORED.value: Settings.EXPLORED_COLOR,
            GridSymbols.PATH.value: Settings.PATH_FOUND_COLOR,
            GridSymbols.START.value: Settings.AGENT_COLOR,
            GridSymbols.DESTINATION.value: Settings.DESTINATION_COLOR
        }
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                self.__draw_grid_rect(x, y, cell_colors[self.maze.grid[y][x]])

    def __draw_key_definition(self):
        """Draw key definition label"""
        label1 = self.font.render(f"1: Drawing mode: {self.drawing_mode.name.capitalize()}", True, Colors.BLACK)
        label2 = self.font.render(f"L: Load empty, S: Save maze", True, Colors.BLACK)
        label3 = self.font.render(f"2: Search algorythm: {self.search_algorythm.value}", True, Colors.BLACK)
        label4 = self.font.render(f"3: Solve maze!", True, Colors.BLACK)
        self.screen.blit(label1, (10, 10))
        self.screen.blit(label2, (10, 30))
        self.screen.blit(label3, (250, 10))
        self.screen.blit(label4, (250, 30))

    # Draw load button
    # def draw_load_button():
    #     button_rect = pygame.Rect(490, 10, 100, 30)
    #     pygame.draw.rect(screen, Colors.GREEN, button_rect, border_radius=5)
    #     label_text = "Load Maze"
    #     label = font.render(label_text, True, Colors.BLACK)
    #     label_rect = label.get_rect(center=button_rect.center)
    #     screen.blit(label, label_rect)

    # font = pygame.font.Font(None, 24)
    # label = font.render("Load Maze", True, BLACK)
    # rect = label.get_rect()
    # rect.center = (WIDTH // 2, HEIGHT - 25)
    # pygame.draw.rect(screen, GREEN, rect, border_radius=5)
    # screen.blit(label, rect)
    def __draw_cursor(self):
        """Draw cursor"""
        self.__draw_grid_rect(*Scene.__get_grid_cords(*pygame.mouse.get_pos()), Colors.GREEN)

    def __solve_maze(self):

        def fill_cells(cells_fill_list, fill_value, delay):
            for cell_ in cells_fill_list:
                self.maze.grid[cell_.coords.height][cell_.coords.width] = fill_value
                self.render()
                sleep(delay)

        if not all((self.maze.get_agent_coords(), self.maze.get_destination_coords())):
            return
        self.maze.clear_explored()
        moves, path = self.maze.solve(self.search_algorythm.value)
        fill_cells(moves, GridSymbols.EXPLORED.value, 0.005)
        fill_cells(path, GridSymbols.PATH.value, 0)

    def render(self):
        self.screen.fill(Colors.WHITE)
        self.__draw_maze()
        self.__draw_cursor()
        self.__draw_key_definition()
        pygame.display.flip()  # Update the display

    def handle_events(self, event):
        """Handle events in game"""

        def on_mousedown():
            # Set the mouse_pressed flag to True
            if event.button == 1:
                self.mouse_pressed = True
                self.erasing_mode = False
            elif event.button == 2:
                self.maze.clear()
            elif event.button == 3:
                self.mouse_pressed = True
                self.erasing_mode = True
            on_mousemotion()

        def on_mouseup():
            # Set the mouse_pressed flag to False
            self.mouse_pressed = False

        def on_mousemotion():
            if self.mouse_pressed:
                grid_coords = Scene.__get_grid_cords(*pygame.mouse.get_pos())
                if self.erasing_mode:
                    self.maze.clear_cell(*grid_coords)
                elif self.drawing_mode == SceneDrawingModes.WALLS:
                    self.maze.set_wall(*grid_coords)
                elif self.drawing_mode == SceneDrawingModes.AGENT:
                    self.maze.set_agent_coords(*grid_coords)
                elif self.drawing_mode == SceneDrawingModes.DESTINATION:
                    self.maze.set_destination_coords(*grid_coords)

        def on_keydown():
            # if event.unicode == "1":
            #     drawing_mode = 1
            if event.key == pygame.K_1:
                self.drawing_mode = self.drawing_mode.next()
            elif event.key == pygame.K_2:
                self.search_algorythm = self.search_algorythm.next()
            elif event.key == pygame.K_3:
                self.__solve_maze()
            elif event.key == pygame.K_s:
                self.maze.save()
            elif event.key == pygame.K_l:
                self.maze.load()

        if event.type == pygame.MOUSEBUTTONDOWN:
            on_mousedown()
        elif event.type == pygame.MOUSEBUTTONUP:
            on_mouseup()
        elif event.type == pygame.MOUSEMOTION:
            on_mousemotion()
        elif event.type == pygame.KEYDOWN:
            on_keydown()
