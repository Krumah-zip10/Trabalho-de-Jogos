import pygame
<<<<<<< HEAD

pygame.init()
WIDTH = 800; HEIGHT = 600
HIT_RADIUS = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))

from player import Player, Morto
from enemy import Enemy
from events import EventHandler
from wave_manager import WaveManager
from projectile import Projectile
=======
from player import Player
from bullet import sinBullet
from util import EventHandler

#inicialização

pygame.init()
WIDTH   =  800; HEIGHT =  600
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))  
player = Player((50, 50))
b = sinBullet((400, 300), -45, life_time=240) 

objects = []
objects.append(player)
objects.append(b)

>>>>>>> upstream/main

clock = pygame.time.Clock()
font_big = pygame.font.SysFont(None, 64)
font_small = pygame.font.SysFont(None, 32)


def new_game():
    player = Player((WIDTH // 2, HEIGHT // 2))
    handler = EventHandler()
    wave_manager = WaveManager(handler, player, WIDTH, HEIGHT)
    objects = [player]
    return player, handler, wave_manager, objects


player, handler, wave_manager, objects = new_game()
game_over = False


def handle_input():
    global game_over, player, handler, wave_manager, objects

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
<<<<<<< HEAD
            if game_over:
                if event.key == pygame.K_r:
                    player, handler, wave_manager, objects = new_game()
                    game_over = False
                continue

=======
            if event.key == pygame.K_SPACE:
                player.action_1() # pode ser melhorado para evento
>>>>>>> upstream/main
            if event.key == pygame.K_TAB:
                player.action_2() # pode ser melhorado para evento

<<<<<<< HEAD
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            player.action_1()
        elif event.type == pygame.MOUSEBUTTONUP and not game_over:
            player.action_1()
=======
def remove_obj(obj):
    #variavel global é feio, mas serve como um exemplo
    if obj in objects:
        objects.remove(obj) 

#inscreve esse metodo pra remoção de objetos
EventHandler().subscribe("DestroyObj", remove_obj)
>>>>>>> upstream/main


running = True
while running:
    dt = clock.tick(60) / 1000

    handle_input()

    if not game_over:
        objects.extend(wave_manager.collect_new_enemies())
        objects.extend(player.collect_new_projectiles())

        for obj in objects:
            obj.update(dt)

        for obj in objects:
            if isinstance(obj, Projectile) and not obj.hit:
                for other in objects:
                    if isinstance(other, Enemy) and not other.pronto_pra_remover():
                        if (obj.pos - other.pos).length() <= HIT_RADIUS:
                            other.take_damage(obj.damage)
                            obj.hit = True
                            break

        objects[:] = [o for o in objects
                      if not (hasattr(o, 'pronto_pra_remover') and o.pronto_pra_remover())]

        if isinstance(player.state, Morto):
            game_over = True

    screen.fill((30, 30, 30))
    for obj in objects:
        obj.draw(screen)
<<<<<<< HEAD

    if game_over:
        texto = font_big.render("GAME OVER", True, (255, 255, 255))
        rect = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        screen.blit(texto, rect)

        texto2 = font_small.render("Aperte R para reiniciar", True, (200, 200, 200))
        rect2 = texto2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(texto2, rect2)

    pygame.display.flip()
=======
    
    pygame.display.flip()
    clock.tick(60)
    
>>>>>>> upstream/main
