import pygame
from config import *
from world import world

class game:
    def __init__(self) -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.clock = pygame.time.Clock()
        self.world = world()
        self.running = True

    def update(self, dt) -> None:
        self.world.update(dt)

    def render(self) -> None:
        self.world.render(self.screen)

    def handle_events(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.world.new_territory(pos)

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