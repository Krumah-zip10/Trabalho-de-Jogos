import pygame
from bolinha import Ball
from shape import Polygon
from collision import Collide
from bonus import BonusZone
from launcher import Launcher
from pegs import gerar_campo

pygame.init()
WIDTH, HEIGHT = 850, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 64)

launcher = Launcher((WIDTH // 2, 40))
bolinha = None

pegs = gerar_campo(WIDTH, n_linhas=8, n_amarelos=6)

parede_esquerda = Polygon([(0, 0), (10, 0), (10, HEIGHT), (0, HEIGHT)])
parede_direita = Polygon([(WIDTH - 10, 0), (WIDTH, 0), (WIDTH, HEIGHT), (WIDTH - 10, HEIGHT)])
parede_topo = Polygon([(0, 0), (WIDTH, 0), (WIDTH, 10), (0, 10)])
paredes = [parede_esquerda, parede_direita, parede_topo]

# campo de pinos termina em y ≈ 380 (100 + 7*40)

triangulo = Polygon([
    (WIDTH // 2 - 25, 420),
    (WIDTH // 2 + 25, 420),
    (WIDTH // 2, 460),
])
obstaculos_fixos = [triangulo]

cx = WIDTH // 2
zona_bonus_esquerda = BonusZone([
    (cx - 200, 545),
    (cx - 150, 520),
    (cx - 100, 545),
    (cx - 150, 570),
], score=50, speed_boost=1.3)

zona_bonus_direita = BonusZone([
    (cx + 100, 545),
    (cx + 150, 520),
    (cx + 200, 545),
    (cx + 150, 570),
], score=50, speed_boost=1.3)

zonas_bonus = [zona_bonus_esquerda, zona_bonus_direita]

FAIXA_LARGURA = WIDTH / 3
PONTOS_FAIXA = [100, 300, 100]

score = 0
bolinhas_restantes = 5
estado_jogo = "jogando"


def amarelos_vivos():
    return any(p.alive and p.kind == 'amarelo' for p in pegs)


running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and bolinha is None and estado_jogo == "jogando":
            if bolinhas_restantes > 0:
                bolinha = Ball(launcher.position)
                bolinha.velocity = launcher.get_launch_velocity()

    if estado_jogo == "jogando":
        if bolinha is None:
            launcher.update(dt)
        else:
            bolinha.update(dt)

            for parede in paredes:
                resultado = Collide.mtv(bolinha.polygon.points, parede.points)
                if resultado:
                    axis, overlap = resultado
                    bolinha.resolve_collision(axis, overlap, parede.centroid())

            for obstaculo in obstaculos_fixos:
                resultado = Collide.mtv(bolinha.polygon.points, obstaculo.points)
                if resultado:
                    axis, overlap = resultado
                    bolinha.resolve_collision(axis, overlap, obstaculo.centroid())

            for peg in pegs:
                if not peg.alive:
                    continue
                resultado = Collide.mtv(bolinha.polygon.points, peg.polygon.points)
                if resultado:
                    axis, overlap = resultado
                    bolinha.resolve_collision(axis, overlap, peg.polygon.centroid())
                    peg.alive = False
                    score += peg.score

            for zona in zonas_bonus:
                score += zona.check(bolinha)

            if bolinha.polygon.centroid().y > HEIGHT:
                faixa = int(bolinha.polygon.centroid().x // FAIXA_LARGURA)
                faixa = max(0, min(2, faixa))
                score += PONTOS_FAIXA[faixa]
                bolinha = None
                bolinhas_restantes -= 1

        if not amarelos_vivos():
            estado_jogo = "venceu"
        elif bolinhas_restantes <= 0 and bolinha is None:
            estado_jogo = "perdeu"

    screen.fill((30, 30, 30))

    for parede in paredes:
        pygame.draw.polygon(screen, (100, 100, 100), parede.points)

    pygame.draw.polygon(screen, (220, 100, 60), triangulo.points)
    pygame.draw.polygon(screen, (255, 255, 255), triangulo.points, 2)

    for peg in pegs:
        peg.draw(screen)

    for zona in zonas_bonus:
        zona.draw(screen)

    if bolinha is None and estado_jogo == "jogando":
        launcher.draw(screen)
    elif bolinha is not None:
        bolinha.draw(screen)

    for i in range(1, 3):
        x = i * FAIXA_LARGURA
        pygame.draw.line(screen, (80, 80, 80), (x, HEIGHT - 40), (x, HEIGHT), 2)

    for i, pontos in enumerate(PONTOS_FAIXA):
        centro_x = int((i + 0.5) * FAIXA_LARGURA)
        texto_faixa = font.render(str(pontos), True, (150, 150, 150))
        rect = texto_faixa.get_rect(center=(centro_x, HEIGHT - 20))
        screen.blit(texto_faixa, rect)

    texto = font.render(f"Score: {score}   Bolinhas: {bolinhas_restantes}", True, (255, 255, 255))
    screen.blit(texto, (10, 10))

    if estado_jogo == "venceu":
        texto_fim = font_big.render("VOCÊ VENCEU!", True, (100, 220, 100))
        rect = texto_fim.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(texto_fim, rect)
    elif estado_jogo == "perdeu":
        texto_fim = font_big.render("GAME OVER", True, (220, 100, 100))
        rect = texto_fim.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(texto_fim, rect)

    pygame.display.flip()

pygame.quit()