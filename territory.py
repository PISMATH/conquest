import pygame

from config import *
from math import sin, cos, pi

class territory:
    def __init__(self, pos, color, alpha) -> None:
        self.points = []
        self.set_inital_points(pos)
        self.color = color
        self.alpha = alpha
        self.growth_rate = territory_base_growth_rate

    def set_inital_points(self, center):
        for i in range(territory_inital_vertices_count):
            angle = 2 * pi * i / territory_inital_vertices_count
            self.points.append(
                [center[0] + sin(angle) * territory_inital_size,
                 center[1] + cos(angle) * territory_inital_size]
            )

    def update(self, dt):
        pass

    def render(self, screen):
        render_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        color = self.color + [self.alpha]
        pygame.draw.polygon(render_surface, color, self.points)
        
        screen.blit(render_surface, (0, 0))