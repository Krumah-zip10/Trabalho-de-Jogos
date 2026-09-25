import pygame
from shape import Polygon
from collision import Collide


class BonusZone:

    def __init__(self, points, score=50, speed_boost=1.0, color=(255, 215, 0)):
        self.polygon = Polygon(points)
        self.score = score
        self.speed_boost = speed_boost
        self.color = color
        self.active = False  

    def check(self, ball):
        colliding = Collide.convex(ball.polygon.points, self.polygon.points)

        if colliding and not self.active:
            self.active = True
            ball.velocity *= self.speed_boost
            return self.score  

        if not colliding:
            self.active = False

        return 0

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.polygon.points)
        pygame.draw.polygon(screen, (255, 255, 255), self.polygon.points, 2)