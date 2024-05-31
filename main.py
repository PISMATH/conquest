import pygame
from config import *
from territory import territory
from images import map_image

class world:
    def __init__(self) -> None:
        self.territories: list[territory] = []

    def update(self, dt) -> None:
        for territory in self.territories:
            territory.update(dt)

    def render(self, screen) -> None:
        screen.blit(map_image, (0, 0))
        for territory in self.territories:
            territory.render(screen)

class game:
    def __init__(self) -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.clock = pygame.time.Clock()
        self.map = world()
        self.running = True

    def update(self, dt) -> None:
        self.map.update(dt)

    def render(self) -> None:
        self.map.render(self.screen)

    def handle_events(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

    def run(self) -> None:
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)

            dt = self.clock.tick() / 1000
            self.update(dt)
            self.render()
            pygame.display.flip()

if __name__ == '__main__':
    Game = game()
    Game.run()