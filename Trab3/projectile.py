import pygame


def colored_sprite(color, size=(8, 8)):
    sprite = pygame.Surface(size)
    sprite.fill(color)
    return sprite


class Projectile:

    def __init__(self, pos, direction, speed=400, damage=1, lifetime=2.0):
        self.pos = pygame.Vector2(pos)
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.lifetime = lifetime
        self.hit = False
        self.sprite = colored_sprite((255, 255, 0))

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.lifetime -= dt

    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

    def pronto_pra_remover(self):
        return self.hit or self.lifetime <= 0