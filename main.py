import pygame
from config import Settings

from scene import Scene


def main():
    # Initialize pygame
    pygame.init()
    scene = Scene()

    # Main game loop
    running = True
    while running:
        scene.clock.tick(Settings.FPS)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene.handle_events(event)
        scene.render()
    pygame.quit()


if __name__ == "__main__":
    main()
