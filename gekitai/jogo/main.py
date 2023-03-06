import pygame
import pygame_gui


def main(papel, ip, porta):
    # constantes
    tamanho_da_janela = (1096, 676)
    cor_de_fundo = (255, 255, 255)

    # inicia pygame e gerenciador de interface
    pygame.init()
    pygame.display.set_caption(f"Gekitai | {papel} ({ip}:{porta})")
    janela = pygame.display.set_mode(tamanho_da_janela)
    gerenciador_de_interface_grafica = pygame_gui.UIManager(tamanho_da_janela)

    # relogio do jogo
    relogio = pygame.time.Clock()

    while True:
        delta_de_tempo = relogio.tick(60)

        # processar input de usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return

            gerenciador_de_interface_grafica.process_events(evento)

        # atualizar estado do jogo
        gerenciador_de_interface_grafica.update(delta_de_tempo / 1000.0)

        # atualizar gráficos
        janela.fill(cor_de_fundo)
        gerenciador_de_interface_grafica.draw_ui(janela)
        pygame.display.update()
