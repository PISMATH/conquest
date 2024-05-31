
from territory import territory
from images import map_image
from config import *

class world:
    def __init__(self) -> None:
        self.territories: list[territory] = []

    def new_territory(self, pos):
        self.territories.append(territory(pos, [255, 0, 0], territory_alpha))

    def update(self, dt) -> None:
        for territory in self.territories:
            territory.update(dt)

    def render(self, screen) -> None:
        screen.blit(map_image, (0, 0))
        for territory in self.territories:
            territory.render(screen)