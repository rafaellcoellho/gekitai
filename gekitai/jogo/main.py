import pygame
import pygame_gui


def main(papel, ip, porta):
    # constantes
    tamanho_da_janela = (936, 655)
    cor_de_fundo = (255, 255, 255)

    # estado inicial do jogo
    turno_do_jogador = "azul"
    estado_do_tabuleiro = [
        ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
        ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
        ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
        ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
        ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
        ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
    ]
    pecas = []

    # carregando assets
    imagem_do_tabuleiro = pygame.image.load("assets/tabuleiro.png")
    imagem_do_retrato_jogador_azul = pygame.transform.smoothscale(
        pygame.image.load("assets/retrato_jogador_azul.png"), (54, 69)
    )
    imagem_do_retrato_jogador_vermelho = pygame.transform.smoothscale(
        pygame.image.load("assets/retrato_jogador_vermelho.png"), (54, 69)
    )
    imagem_da_peca_jogador_azul = pygame.transform.smoothscale(
        pygame.image.load("assets/peca_jogador_azul.png"), (80, 80)
    )
    imagem_da_peca_jogador_vermelho = pygame.transform.smoothscale(
        pygame.image.load("assets/peca_jogador_vermelho.png"), (80, 80)
    )
    imagem_borda_status_turno = pygame.transform.smoothscale(
        pygame.image.load("assets/borda_indicando_status_de_turno.png"), (64, 79)
    )

    # inicia pygame e gerenciador de interface
    pygame.init()
    pygame.display.set_caption(f"Gekitai | {papel} ({ip}:{porta})")
    janela = pygame.display.set_mode(tamanho_da_janela)
    gerenciador_de_interface_grafica = pygame_gui.UIManager(tamanho_da_janela)

    # construir interface gráfica de jogo
    pos_superior_esquerdo_interface_de_jogo = (10, 10)
    interface_de_jogo = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect(pos_superior_esquerdo_interface_de_jogo, (556, 656)),
        manager=gerenciador_de_interface_grafica,
    )

    interface_do_tabuleiro = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect(
            (0, 0), (imagem_do_tabuleiro.get_width(), imagem_do_tabuleiro.get_height())
        ),
        manager=gerenciador_de_interface_grafica,
        container=interface_de_jogo,
    )
    pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (0, 0),
            (imagem_do_tabuleiro.get_width(), imagem_do_tabuleiro.get_height()),
        ),
        image_surface=imagem_do_tabuleiro,
        manager=gerenciador_de_interface_grafica,
        container=interface_do_tabuleiro,
    )

    interface_de_controle_dos_turnos = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect(
            (0, 10),
            (
                imagem_do_tabuleiro.get_width(),
                imagem_do_retrato_jogador_azul.get_height(),
            ),
        ),
        manager=gerenciador_de_interface_grafica,
        container=interface_de_jogo,
        anchors={
            "top": "top",
            "top_target": interface_do_tabuleiro,
        },
    )

    interface_de_status_do_turno = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect((10, 0), (118, 69)),
        manager=gerenciador_de_interface_grafica,
        container=interface_de_controle_dos_turnos,
    )
    retrato_jogador_azul = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (0, 0),
            (
                imagem_do_retrato_jogador_azul.get_width(),
                imagem_do_retrato_jogador_azul.get_height(),
            ),
        ),
        image_surface=imagem_do_retrato_jogador_azul,
        manager=gerenciador_de_interface_grafica,
        container=interface_de_status_do_turno,
    )
    retrato_jogador_vermelho = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (10, 0),
            (
                imagem_do_retrato_jogador_vermelho.get_width(),
                imagem_do_retrato_jogador_vermelho.get_height(),
            ),
        ),
        image_surface=imagem_do_retrato_jogador_vermelho,
        manager=gerenciador_de_interface_grafica,
        container=interface_de_status_do_turno,
        anchors={"left": "left", "left_target": retrato_jogador_azul},
    )

    interface_de_botoes_passar_e_desistir = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect((-200, 0), (200, 69)),
        manager=gerenciador_de_interface_grafica,
        container=interface_de_controle_dos_turnos,
        anchors={"right": "right"},
    )
    botao_de_desistir = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 0), (100, 69)),
        text="Desistir",
        manager=gerenciador_de_interface_grafica,
        container=interface_de_botoes_passar_e_desistir,
    )
    botao_de_passar_turno = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 0), (100, 69)),
        text="Passar",
        manager=gerenciador_de_interface_grafica,
        container=interface_de_botoes_passar_e_desistir,
        anchors={"left": "left", "left_target": botao_de_desistir},
    )

    # construir interface gráfica do chat
    interface_de_chat = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect((10, 10), (350, 634)),
        manager=gerenciador_de_interface_grafica,
        anchors={
            "left": "left",
            "left_target": interface_de_jogo,
        },
    )
    log_de_mensagens = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((0, 0), (interface_de_chat.relative_rect.width, 590)),
        manager=gerenciador_de_interface_grafica,
        container=interface_de_chat,
        html_text="",
    )

    interface_de_entrada_de_texto = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect((0, 5), (interface_de_chat.relative_rect.width, 40)),
        manager=gerenciador_de_interface_grafica,
        container=interface_de_chat,
        anchors={
            "top": "top",
            "top_target": log_de_mensagens,
        },
    )
    entrada_de_texto = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(
            (0, 0), (250, interface_de_entrada_de_texto.relative_rect.height)
        ),
        manager=gerenciador_de_interface_grafica,
        container=interface_de_entrada_de_texto,
    )
    botao_de_enviar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (5, 0), (95, interface_de_entrada_de_texto.relative_rect.height)
        ),
        manager=gerenciador_de_interface_grafica,
        container=interface_de_entrada_de_texto,
        anchors={
            "left": "left",
            "left_target": entrada_de_texto,
        },
        text="Enviar",
    )

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

        retrato_jogador_com_turno_ativo = (
            retrato_jogador_azul
            if turno_do_jogador == "azul"
            else retrato_jogador_vermelho
        )

        # atualizar gráficos
        janela.fill(cor_de_fundo)
        gerenciador_de_interface_grafica.draw_ui(janela)

        janela.blit(
            imagem_borda_status_turno,
            (
                retrato_jogador_com_turno_ativo.rect.left - 5,
                retrato_jogador_com_turno_ativo.rect.top - 5,
            ),
        )

        pygame.display.update()
