import pygame
import os
from abc import ABC, abstractmethod
from projectile import Projectile

SPRITE_DIR = os.path.join("images", "duck")

def load_sprite(name):
    path = os.path.join(SPRITE_DIR, f"{name}.png")
    return pygame.image.load(path).convert_alpha()

INVENCIBILIDADE_DURACAO = 1.0
FLICKER_INTERVALO = 0.1


class Player:

    def __init__(self, pos, max_hp=3):
        self.pos = pygame.Vector2(pos)
        self.max_hp = max_hp
        self.hp = max_hp
        self.state = Base(self)
        self.new_projectiles = []
        self.invincible_timer = 0.0

    def update(self, dt):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def action_1(self):
        self.state.action_1()

    def action_2(self):
        self.state.action_2()

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)

    def take_damage(self, amount):
        if self.invincible_timer > 0 or isinstance(self.state, Morto):
            return
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.change_state(Morto)
        else:
            self.invincible_timer = INVENCIBILIDADE_DURACAO

    def collect_new_projectiles(self):
        pending = self.new_projectiles
        self.new_projectiles = []
        return pending


class PlayerState(ABC):

    sprite = pygame.Surface((32, 32))
    hurt_sprite = None

    def __init__(self, player):
        self.P = player

    def draw(self, screen):
        sprite = self.sprite
        if self.P.invincible_timer > 0 and self.hurt_sprite is not None:
            if int(self.P.invincible_timer / FLICKER_INTERVALO) % 2 == 0:
                sprite = self.hurt_sprite
        screen.blit(sprite, self.P.pos)

    def delete(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def action_1(self):
        pass

    @abstractmethod
    def action_2(self):
        pass


class Base(PlayerState):
    sprite = load_sprite("base")
    hurt_sprite = load_sprite("quack")

    def update(self, dt):
        pass

    def action_1(self):
        self.P.change_state(Atirando)

    def action_2(self):
        self.P.take_damage(1)  # TEMPORÁRIO: só pra validar visualmente


class Atirando(PlayerState):
    sprite = load_sprite("wing")
    hurt_sprite = load_sprite("quack")
    FIRE_RATE = 0.3

    def __init__(self, player):
        super().__init__(player)
        self.timer = 0

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.FIRE_RATE
            self._fire()

    def _fire(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        direcao = mouse_pos - self.P.pos
        if direcao.length() > 0:
            direcao = direcao.normalize()
        self.P.new_projectiles.append(Projectile(self.P.pos, direcao))

    def action_1(self):
        self.P.change_state(Base)

    def action_2(self):
        self.P.take_damage(1)  # TEMPORÁRIO


class Morto(PlayerState):
    sprite = load_sprite("crouch")

    def update(self, dt):
        pass

    def action_1(self):
        pass

    def action_2(self):
        pass