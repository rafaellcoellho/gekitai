from typing import Tuple

import pygame

from pygame.surface import Surface
from pygame.time import Clock

TAMANHO_DA_JANELA: Tuple[int, int] = (500, 300)
COR_DO_BACKGROUND: Tuple[int, int, int] = (100, 100, 100)

COR_DO_CIRCULO: Tuple[int, int, int] = (200, 200, 200)
RAIO_DO_CIRCULO: int = 20


def executar_modo_espera():
    dx: int = 3
    dy: int = 4
    x: int = 100
    y: int = 100

    pygame.init()
    clock: Clock = pygame.time.Clock()
    display: Surface = pygame.display.set_mode(TAMANHO_DA_JANELA, pygame.SRCALPHA, 32)

    while True:
        clock.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return

        display.fill(COR_DO_BACKGROUND)

        x = x + dx
        y = y + dy
        pygame.draw.circle(display, COR_DO_CIRCULO, (x, y), RAIO_DO_CIRCULO)

        if x < RAIO_DO_CIRCULO or x > 500 - RAIO_DO_CIRCULO:
            dx = -dx
        if y < RAIO_DO_CIRCULO or y > 300 - RAIO_DO_CIRCULO:
            dy = -dy

        pygame.display.update()
