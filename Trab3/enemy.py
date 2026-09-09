import pygame
from abc import ABC, abstractmethod

class Enemy:

    def __init__(self, pos, target, handler, max_hp=2, speed=50,
                 contact_radius=20, attack_damage=1, attack_cooldown=1.0):
        self.pos = pygame.Vector2(pos)
        self.target = target
        self.handler = handler
        self.max_hp = max_hp
        self.hp = max_hp
        self.speed = speed
        self.contact_radius = contact_radius
        self.attack_damage = attack_damage
        self.attack_cooldown = attack_cooldown
        self.state = Spawning(self)

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)

    def take_damage(self, amount):
        if isinstance(self.state, Morto):
            return
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.change_state(Morto)
            self.handler.notify('enemy_killed', self)
        else:
            self.change_state(LevandoDano)

    def pronto_pra_remover(self):
        return isinstance(self.state, Morto) and self.state.terminou()


def colored_sprite(color, size=(24, 24)):
    sprite = pygame.Surface(size)
    sprite.fill(color)
    return sprite


class EnemyState(ABC):

    sprite = pygame.Surface((24, 24))

    def __init__(self, enemy):
        self.E = enemy

    def draw(self, screen):
        screen.blit(self.sprite, self.E.pos)

    def delete(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass


class Spawning(EnemyState):
    sprite = colored_sprite((200, 200, 0))
    DURACAO = 0.3

    def __init__(self, enemy):
        super().__init__(enemy)
        self.timer = self.DURACAO

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.E.change_state(Aproximando)


class Aproximando(EnemyState):
    sprite = colored_sprite((200, 0, 0))

    def update(self, dt):
        direcao = self.E.target.pos - self.E.pos
        if direcao.length() > 0:
            direcao = direcao.normalize()
        self.E.pos += direcao * self.E.speed * dt

        if (self.E.target.pos - self.E.pos).length() <= self.E.contact_radius:
            self.E.change_state(Atacando)


class Atacando(EnemyState):
    sprite = colored_sprite((150, 0, 150))

    def __init__(self, enemy):
        super().__init__(enemy)
        self.timer = 0

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.E.attack_cooldown
            self.E.target.take_damage(self.E.attack_damage)


class LevandoDano(EnemyState):
    sprite = colored_sprite((255, 255, 255))
    DURACAO = 0.2

    def __init__(self, enemy):
        super().__init__(enemy)
        self.timer = self.DURACAO

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            distancia = (self.E.target.pos - self.E.pos).length()
            if distancia <= self.E.contact_radius:
                self.E.change_state(Atacando)
            else:
                self.E.change_state(Aproximando)


class Morto(EnemyState):
    sprite = colored_sprite((50, 50, 50))
    DURACAO = 0.3

    def __init__(self, enemy):
        super().__init__(enemy)
        self.timer = self.DURACAO

    def update(self, dt):
        self.timer -= dt

    def terminou(self):
        return self.timer <= 0