import pygame
from grid import Grid, Cell


pygame.init()
pygame.font.init()

WIDTH   =  800; HEIGHT =  600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  

relogio = pygame.time.Clock()
grid_size = (10, 10)
grid = Grid(0, 0, None, grid_size)

WIDTH   =  800; HEIGHT =  600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  

objects = []

while True: 
    relogio.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if grid.botao_pausa.collidepoint(event.pos):
                    grid.pausado = not grid.pausado
                elif grid.game_over and grid.botao_reiniciar.collidepoint(event.pos):
                    grid.reiniciar()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_w:
                grid.definir_direcao(-1, 0)
            if event.key == pygame.K_s:
                grid.definir_direcao(1, 0)
            if event.key == pygame.K_a:
                grid.definir_direcao(0, -1)
            if event.key == pygame.K_d:
                grid.definir_direcao(0, 1)

    for obj in objects:
        obj.update(1)

    grid.update(1)

    screen.fill((30, 30, 30))

    for obj in objects:
        obj.draw()

    grid.draw(screen)
    pygame.display.flip()