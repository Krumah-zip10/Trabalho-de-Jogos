import pygame
from shape import Polygon, regular_polygon

GRAVITY = pygame.Vector2(0, 500)


class Ball:

    def __init__(self, center, radius=15, sides=6):
        self.polygon = Polygon(regular_polygon(center, radius, sides))
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        self.velocity += GRAVITY * dt
        self.polygon.translate(self.velocity.x * dt, self.velocity.y * dt)

    def centroid(self):
        return self.polygon.centroid()

    def resolve_collision(self, axis, overlap, other_centroid):
        normal = pygame.Vector2(axis)

        direction = self.centroid() - other_centroid
        if direction.dot(normal) < 0:
            normal = -normal

        self.polygon.translate(normal.x * overlap, normal.y * overlap)
        self.velocity = self.velocity.reflect(normal)

    def draw(self, screen, color=(60, 120, 220)):
        pygame.draw.polygon(screen, color, self.polygon.points)
        pygame.draw.polygon(screen, (255, 255, 255), self.polygon.points, 2)