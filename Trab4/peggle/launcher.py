import pygame
import math


class Launcher:

    def __init__(self, position, min_angle=-70, max_angle=70,
                 swing_speed=90, launch_speed=400):
        self.position = pygame.Vector2(position)
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.angle = 0  
        self.direction = 1
        self.swing_speed = swing_speed  
        self.launch_speed = launch_speed

    def update(self, dt):
        self.angle += self.direction * self.swing_speed * dt
        if self.angle >= self.max_angle:
            self.angle = self.max_angle
            self.direction = -1
        elif self.angle <= self.min_angle:
            self.angle = self.min_angle
            self.direction = 1

    def get_launch_velocity(self):
        rad = math.radians(self.angle)
        vx = self.launch_speed * math.sin(rad)
        vy = self.launch_speed * math.cos(rad)
        return pygame.Vector2(vx, vy)

    def draw(self, screen):
        rad = math.radians(self.angle)
        end = self.position + pygame.Vector2(
            40 * math.sin(rad), 40 * math.cos(rad)
        )
        pygame.draw.line(screen, (255, 255, 255), self.position, end, 3)
        pygame.draw.circle(screen, (200, 200, 200), self.position, 6)