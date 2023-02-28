from typing import Tuple

import pygame

from pygame.surface import Surface
from pygame.time import Clock


TAMANHO_DA_JANELA: Tuple[int, int] = (500, 300)
COR_DO_BACKGROUND: Tuple[int, int, int] = (100, 100, 100)

COR_DO_CIRCULO: Tuple[int, int, int] = (200, 200, 200)
RAIO_DO_CIRCULO: int = 20


class Jogo:
    def __init__(self):
        self.executando: bool = False
        self.dx: int = 3
        self.dy: int = 4
        self.x: int = 100
        self.y: int = 100

        self.relogio: Clock = pygame.time.Clock()
        self.display: Surface = pygame.display.set_mode(
            TAMANHO_DA_JANELA, pygame.SRCALPHA, 32
        )

    def run(self):
        pygame.init()
        self.executando = True

        while self.executando:
            self.processar_entrada_de_usuario()
            self.atualizar_estado()
            self.atualizar_graficos()
            self.relogio.tick(30)

    def processar_entrada_de_usuario(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False

    def atualizar_estado(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        if self.x < RAIO_DO_CIRCULO or self.x > 500 - RAIO_DO_CIRCULO:
            self.dx = -self.dx
        if self.y < RAIO_DO_CIRCULO or self.y > 300 - RAIO_DO_CIRCULO:
            self.dy = -self.dy

    def atualizar_graficos(self):
        self.display.fill(COR_DO_BACKGROUND)
        pygame.draw.circle(
            self.display, COR_DO_CIRCULO, (self.x, self.y), RAIO_DO_CIRCULO
        )
        pygame.display.update()


def executar_logo_quicando():
    game = Jogo()
    game.run()
