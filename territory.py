import pygame

from config import *
from math import sin, cos, sqrt, pi

class territory:
    def __init__(self, pos, color, alpha) -> None:
        self.points = []
        self.active_point_indices = []
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
        
        self.active_point_indices = list(range(territory_inital_vertices_count))
    
    def find_normal(self, index):
        x1, y1 = self.points[index - 1]
        x2, y2 = self.points[(index + 1) % len(self.points)]
        
        x_diff = x1 - x2
        y_diff = y1 - y2

        div = sqrt(x_diff ** 2 + y_diff ** 2)
        if div == 0:
            return 0, 0
        return y_diff / div, -x_diff / div

    def update(self, dt):
        move_dist = dt * self.growth_rate
        for index in self.active_point_indices:
            p_x, p_y = self.points[index]
            normal_x, normal_y = self.find_normal(index)
            new_point = [p_x + normal_x * self.growth_rate, p_y + normal_y * self.growth_rate]
            self.points[index] = new_point

    def render(self, screen):
        render_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        color = self.color + [self.alpha]
        pygame.draw.polygon(render_surface, color, self.points)
        
        screen.blit(render_surface, (0, 0))
        for i, point in enumerate(self.points):
            pygame.draw.circle(screen, (((len(self.points) - i) * 255) // len(self.points), 0, (i * 255) // len(self.points)), point, 2)