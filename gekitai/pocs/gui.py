import pygame
import pygame_gui


def executar_exemplo_gui_tela_de_jogo():
    pygame.init()

    pygame.display.set_caption("Exemplo GUI da tela de jogo")
    janela = pygame.display.set_mode((800, 600))

    fundo = pygame.Surface((800, 600))
    fundo.fill(pygame.Color("#000000"))

    gerenciador_de_interface = pygame_gui.UIManager((800, 600))

    botao = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 275), (100, 50)),
        text="Foo",
        manager=gerenciador_de_interface,
    )

    relogio = pygame.time.Clock()

    while True:
        variacao_de_tempo = relogio.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            if evento.type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == botao:
                    print("Bar!")

            gerenciador_de_interface.process_events(evento)

        gerenciador_de_interface.update(variacao_de_tempo)

        janela.blit(fundo, (0, 0))
        gerenciador_de_interface.draw_ui(janela)

        pygame.display.update()
