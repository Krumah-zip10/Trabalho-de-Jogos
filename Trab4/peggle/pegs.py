import random
import pygame
from shape import Polygon, regular_polygon


class Peg:

    def __init__(self, points, kind='azul', score=10):
        self.polygon = Polygon(points)
        self.kind = kind
        self.score = score
        self.alive = True
        self.color = (230, 200, 40) if kind == 'amarelo' else (60, 140, 220)

    def draw(self, screen):
        if not self.alive:
            return
        pygame.draw.polygon(screen, self.color, self.polygon.points)
        pygame.draw.polygon(screen, (255, 255, 255), self.polygon.points, 2)


def gerar_campo(width, n_linhas=8, n_amarelos=6,
                start_y=100, row_spacing=40,
                start_x=130, col_spacing=90):
    posicoes = []
    for linha in range(n_linhas):
        y = start_y + linha * row_spacing
        offset = col_spacing // 2 if linha % 2 else 0
        x = start_x + offset
        while x < width - start_x:
            posicoes.append((x, y))
            x += col_spacing

    random.shuffle(posicoes)
    amarelas = set(posicoes[:n_amarelos])

    pegs = []
    for pos in posicoes:
        kind = 'amarelo' if pos in amarelas else 'azul'
        score = 100 if kind == 'amarelo' else 10
        pontos = regular_polygon(pos, 16, 6)
        pegs.append(Peg(pontos, kind, score))

    return pegs