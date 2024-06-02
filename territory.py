import pygame

from config import *
from math import sin, cos, sqrt, pi

class territory:
    def __init__(self, pos, color, alpha) -> None:
        self.points = []
        self.active_point_indices = set()
        self.set_inital_points(pos)
        self.color = color
        self.alpha = alpha
        self.growth_rate = territory_base_growth_rate

    def dist_sqr(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    
    def mid_point(self, p1, p2):
        return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

    def set_inital_points(self, center):
        for i in range(territory_inital_vertices_count):
            angle = 2 * pi * i / territory_inital_vertices_count
            self.points.append(
                [center[0] + sin(angle) * territory_inital_size,
                 center[1] + cos(angle) * territory_inital_size]
            )
        
        self.active_point_indices = set(range(territory_inital_vertices_count))
    
    def add_point(self, index, point):
        self.points.insert(index, point)
        for i, point_index in enumerate(self.active_point_indices.copy()):
            if point_index >= index:
                new_index = (point_index + 1) % len(self.points)
                self.active_point_indices.add(new_index)
        
        self.active_point_indices.add(index)
        
    def find_normal(self, index):
        x1, y1 = self.points[index - 1]
        x2, y2 = self.points[(index + 1) % len(self.points)]
        
        x_diff = x1 - x2
        y_diff = y1 - y2

        div = sqrt(x_diff ** 2 + y_diff ** 2)
        if div == 0:
            return 0, 0
        return y_diff / div, -x_diff / div
    
    def point_in_area(self, point) -> bool:
        x, y = point
        n = len(self.points)
        inside = False

        p1x, p1y = self.points[0]
        for i in range(1, n + 1):
            p2x, p2y = self.points[i % n]
            if min(p1y, p2y) < y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

                if p1x == p2x or x <= xinters:
                    inside = not inside

            p1x, p1y = p2x, p2y

        return inside

    def update(self, dt, other_territories):
        # intersect
        for territory in other_territories:
            if territory == self:
                continue
            for index in self.active_point_indices.copy():
                point = self.points[index]
                if territory.point_in_area(point):
                    self.active_point_indices.remove(index)
        
        # grow
        move_dist = dt * self.growth_rate
        for index in self.active_point_indices:
            p_x, p_y = self.points[index]
            normal_x, normal_y = self.find_normal(index)
            new_point = [p_x + normal_x * move_dist, p_y + normal_y * move_dist]
            self.points[index] = new_point
        
        # split
        for i, point in enumerate(self.points):
            second_point = self.points[i - 1]
            if self.dist_sqr(point, second_point) > territory_line_max_len ** 2:
                mid_point = self.mid_point(point, second_point)
                self.add_point(i, mid_point)
            
    def render(self, screen):
        render_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        color = self.color + [self.alpha]
        pygame.draw.polygon(render_surface, color, self.points)
        
        screen.blit(render_surface, (0, 0))
        for i, point in enumerate(self.points):
            pygame.draw.circle(screen, (((len(self.points) - i) * 255) // len(self.points), 0, (i * 255) // len(self.points)), point, 2)