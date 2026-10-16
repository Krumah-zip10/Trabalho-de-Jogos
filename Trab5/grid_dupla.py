import pygame

TILE = 40


MAPA_TEXTO = [
    "####################",
    "#..................#",
    "#..###.......#.....#",
    "#..###.......#.....#",
    "#..###.............#",
    "#..................#",
    "#.......#.#.#......#",
    "#........#.#.......#",
    "#.......#.#.#......#",
    "#..........#.......#",
    "#....#####.#.......#",
    "#....#...#.....#...#",
    "#....#...#.....#...#",
    "#....#####.........#",
    "####################",
]
ALTURA = len(MAPA_TEXTO)
LARGURA = len(MAPA_TEXTO[0])
assert all(len(l) == LARGURA for l in MAPA_TEXTO)


mundo = [[c == '#' for c in linha] for linha in MAPA_TEXTO]


FORA_E_COLISAO = True

PEDRA = (110, 110, 120)
GRAMA = (90, 160, 80)
BORDA = (40, 40, 50)


def celula(l, c):
    if 0 <= l < ALTURA and 0 <= c < LARGURA:
        return mundo[l][c]
    return FORA_E_COLISAO


def indice(i, j):
    return (int(celula(i - 1, j - 1))
            | int(celula(i - 1, j)) << 1
            | int(celula(i, j - 1)) << 2
            | int(celula(i, j)) << 3)


def gerar_sprite(idx, t):
    tl, tr, bl, br = idx & 1, (idx >> 1) & 1, (idx >> 2) & 1, (idx >> 3) & 1
    s = pygame.Surface((t, t))
    for py in range(t):
        y = (py + 0.5) / t
        for px in range(t):
            x = (px + 0.5) / t
            w = (tl * (1 - x) * (1 - y) + tr * x * (1 - y)
                 + bl * (1 - x) * y + br * x * y)
            if abs(w - 0.5) < 0.04:
                cor = BORDA
            elif w > 0.5:
                cor = PEDRA
            else:
                cor = GRAMA
            s.set_at((px, py), cor)
    return s


sprites = None
visual = None


def preparar():
    global sprites, visual
    sprites = [gerar_sprite(i, TILE) for i in range(16)]
    visual = [[indice(i, j) for j in range(LARGURA + 1)]
              for i in range(ALTURA + 1)]


def desenhar(tela, jogador, debug, fonte):
    tela.fill(GRAMA)
    for i in range(ALTURA + 1):
        for j in range(LARGURA + 1):

            tela.blit(sprites[visual[i][j]],
                      (j * TILE - TILE // 2, i * TILE - TILE // 2))
    if debug:
        sup = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        sup.fill((255, 0, 0, 90))
        for l in range(ALTURA):
            for c in range(LARGURA):
                if mundo[l][c]:
                    tela.blit(sup, (c * TILE, l * TILE))
        for i in range(ALTURA + 1):
            for j in range(LARGURA + 1):
                txt = fonte.render(str(visual[i][j]), True, (255, 255, 255))
                tela.blit(txt, (j * TILE - txt.get_width() // 2,
                                i * TILE - txt.get_height() // 2))
    pygame.draw.rect(tela, (230, 200, 50), jogador)
    pygame.draw.rect(tela, BORDA, jogador, 2)


def colide(r):
    for l in range(r.top // TILE, (r.bottom - 1) // TILE + 1):
        for c in range(r.left // TILE, (r.right - 1) // TILE + 1):
            if celula(l, c):
                return True
    return False


def mover(r, dx, dy):
    r.x += dx
    if colide(r):
        r.x -= dx
    r.y += dy
    if colide(r):
        r.y -= dy


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA * TILE, ALTURA * TILE))
    pygame.display.set_caption("Grid dupla  (D = debug, ESC = sair)")
    fonte = pygame.font.SysFont(None, 18)
    clock = pygame.time.Clock()
    preparar()
    jogador = pygame.Rect(TILE + 10, TILE + 10, 20, 20)
    debug = False
    rodando = True
    while rodando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    rodando = False
                elif e.key == pygame.K_d:
                    debug = not debug
        k = pygame.key.get_pressed()
        mover(jogador, (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * 3,
              (k[pygame.K_DOWN] - k[pygame.K_UP]) * 3)
        desenhar(tela, jogador, debug, fonte)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()