import pygame
from abc import ABC, abstractmethod
from random import randint


class obj(ABC):

    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.sprites = sprites

    def draw(self, screen):
        for s in self.sprites:
            screen.blit(s, (self.x, self.y))

    @abstractmethod
    def update(self, dt):
        pass


class Grid(obj):

    def __init__(self, x, y, sprites, grid_size):
        super().__init__(x, y, sprites)
        num_linhas, num_colunas = grid_size
        self.tamanho_celula = 50

        self.cells = []
        for linha in range(num_linhas):
            linha_de_celulas = []
            for coluna in range(num_colunas):
                px = coluna * self.tamanho_celula
                py = linha * self.tamanho_celula
                celula = Cell(px, py, sprites, grid_size)
                linha_de_celulas.append(celula)
            self.cells.append(linha_de_celulas)

        self.game_over = False
        self.pausado = True
        self.botao_pausa = pygame.Rect(600, 20, 150, 40)
        self.botao_reiniciar = pygame.Rect(600, 80, 150, 40)
        self.fonte = pygame.font.SysFont("arial", 35, True, True)
        self.reiniciar()

    def draw(self, screen):
        for linha_de_celulas in self.cells:
            for celula in linha_de_celulas:
                celula.draw(screen)
        cor_botao = (100, 100, 200) if not self.pausado else (200, 100, 100)
        pygame.draw.rect(screen, cor_botao, self.botao_pausa)
        texto_pause = self.fonte.render("PAUSE", True, (255, 255, 255))
        screen.blit(texto_pause, (625, 20))

        if self.game_over:
            texto_game_over = self.fonte.render("GAME OVER (Aperte para reiniciar)", True, (255, 255, 255))
            screen.blit(texto_game_over, (150, 250))
            pygame.draw.rect(screen, (150, 150, 150), self.botao_reiniciar)
            texto_reiniciar = self.fonte.render("RESTART", True, (255, 255, 255))
            screen.blit(texto_reiniciar, (605, 80))

    def update(self, dt):
        if self.game_over or self.pausado:
            return

        cabeca_linha, cabeca_coluna = self.cobra[-1]
        delta_linha, delta_coluna = self.direcao
        nova_cabeca = (cabeca_linha + delta_linha, cabeca_coluna + delta_coluna)

        num_linhas = len(self.cells)
        num_colunas = len(self.cells[0])
        saiu_da_grade = not (0 <= nova_cabeca[0] < num_linhas and 0 <= nova_cabeca[1] < num_colunas)

        if saiu_da_grade or nova_cabeca in self.cobra:
            self.game_over = True
            return

        comeu = (nova_cabeca == self.maca_pos)
        self.cobra.append(nova_cabeca)
        self.cells[nova_cabeca[0]][nova_cabeca[1]].estado = "cobra"

        if comeu:
            self.maca_pos = self.gerar_posicao_maca()
            self.cells[self.maca_pos[0]][self.maca_pos[1]].estado = "maca"
        else:
            rabo_linha, rabo_coluna = self.cobra[0]
            self.cells[rabo_linha][rabo_coluna].estado = "vazia"
            del self.cobra[0]

    def gerar_posicao_maca(self):
        num_linhas = len(self.cells)
        num_colunas = len(self.cells[0])
        linha = randint(0, num_linhas - 1)
        coluna = randint(0, num_colunas - 1)
        return (linha, coluna)

    def definir_direcao(self, delta_linha, delta_coluna):
        oposto = (-self.direcao[0], -self.direcao[1])
        if (delta_linha, delta_coluna) == oposto:
            return
        self.direcao = (delta_linha, delta_coluna)

    def reiniciar(self):
        for linha_de_celulas in self.cells:
            for celula in linha_de_celulas:
                celula.estado = "vazia"

        cabeca = (2, 5)
        self.direcao = (0, 1)
        rabo = (cabeca[0] - self.direcao[0], cabeca[1] - self.direcao[1])

        self.cobra = [rabo, cabeca]
        self.cells[cabeca[0]][cabeca[1]].estado = "cobra"
        self.cells[rabo[0]][rabo[1]].estado = "cobra"

        self.maca_pos = self.gerar_posicao_maca()
        self.cells[self.maca_pos[0]][self.maca_pos[1]].estado = "maca"

        self.game_over = False
        self.pausado = True


class Cell(obj):

    def __init__(self, x, y, sprites, grid_size):
        super().__init__(x, y, sprites)
        self.estado = "vazia"

    def draw(self, screen):
        if self.estado == "cobra":
            cor = (0, 255, 0)
        elif self.estado == "maca":
            cor = (255, 0, 0)
        else:
            cor = (80, 80, 80)
        pygame.draw.rect(screen, cor, (self.x, self.y, 50, 50))

    def update(self, dt):
        return