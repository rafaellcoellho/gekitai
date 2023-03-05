import pygame
import pygame_gui
import math


def modo_exemplo_interface_de_jogo():
    pygame.init()

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

    tamanho_da_janela = (575, 656)
    janela = pygame.display.set_mode(tamanho_da_janela)
    janela.fill((255, 255, 255))

    gerenciador_interface_grafica = pygame_gui.UIManager(tamanho_da_janela)

    pos_inicial_tabuleiro = (10, 10)
    interface_de_jogo = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect(pos_inicial_tabuleiro, (556, 656)),
        manager=gerenciador_interface_grafica,
    )

    # tabuleiro
    interface_do_tabuleiro = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect(
            (0, 0), (imagem_do_tabuleiro.get_width(), imagem_do_tabuleiro.get_height())
        ),
        manager=gerenciador_interface_grafica,
        container=interface_de_jogo,
    )
    tabuleiro = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (0, 0),
            (imagem_do_tabuleiro.get_width(), imagem_do_tabuleiro.get_height()),
        ),
        image_surface=imagem_do_tabuleiro,
        manager=gerenciador_interface_grafica,
        container=interface_do_tabuleiro,
    )

    # interface de controle dos turnos
    interface_de_controle_dos_turnos = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect(
            (0, 10),
            (
                imagem_do_tabuleiro.get_width(),
                imagem_do_retrato_jogador_azul.get_height(),
            ),
        ),
        manager=gerenciador_interface_grafica,
        container=interface_de_jogo,
        anchors={
            "top": "top",
            "top_target": interface_do_tabuleiro,
        },
    )

    # status do turno
    interface_de_status_do_turno = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect((10, 0), (118, 69)),
        manager=gerenciador_interface_grafica,
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
        manager=gerenciador_interface_grafica,
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
        manager=gerenciador_interface_grafica,
        container=interface_de_status_do_turno,
        anchors={"left": "left", "left_target": retrato_jogador_azul},
    )

    # botoes de passar e desistir
    interface_de_botoes_passar_e_desistir = pygame_gui.core.UIContainer(
        relative_rect=pygame.Rect((-200, 0), (200, 69)),
        manager=gerenciador_interface_grafica,
        container=interface_de_controle_dos_turnos,
        anchors={"right": "right"},
    )
    botao_de_desistir = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 0), (100, 69)),
        text="Desistir",
        manager=gerenciador_interface_grafica,
        container=interface_de_botoes_passar_e_desistir,
    )
    botao_de_passar_turno = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 0), (100, 69)),
        text="Passar",
        manager=gerenciador_interface_grafica,
        container=interface_de_botoes_passar_e_desistir,
        anchors={"left": "left", "left_target": botao_de_desistir},
    )

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == botao_de_desistir:
                        print("desistir do jogo")
                    elif event.ui_element == botao_de_passar_turno:
                        turno_do_jogador = (
                            "vermelho" if turno_do_jogador == "azul" else "azul"
                        )
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                posicao_do_mouse = pygame.mouse.get_pos()

                tamanho_offset_borda_externa = (11, 11)
                tamanho_offset_borda_interna = (10, 10)
                lado_quadrados = (87, 87)

                # pos_superior_esquerdo_considerando_borda =
                pos_superior_esquerdo_considerando_borda = (
                    pos_inicial_tabuleiro[0]
                    + tamanho_offset_borda_externa[0]
                    + tamanho_offset_borda_interna[0]
                ), (
                    pos_inicial_tabuleiro[1]
                    + tamanho_offset_borda_externa[1]
                    + tamanho_offset_borda_interna[1]
                )
                pos_inferior_direito_considerando_borda = (
                    pos_superior_esquerdo_considerando_borda[0]
                    + (6 * lado_quadrados[0]),
                    pos_superior_esquerdo_considerando_borda[1]
                    + (6 * lado_quadrados[1]),
                )

                clicou_dentro_do_tabuleiro = (
                    pos_superior_esquerdo_considerando_borda[0]
                    <= posicao_do_mouse[0]
                    <= pos_inferior_direito_considerando_borda[0]
                    and pos_superior_esquerdo_considerando_borda[1]
                    <= posicao_do_mouse[1]
                    <= pos_inferior_direito_considerando_borda[1]
                )

                if clicou_dentro_do_tabuleiro:
                    pos_mouse_no_tabuleiro_considerando_borda = (
                        posicao_do_mouse[0]
                        - pos_superior_esquerdo_considerando_borda[0],
                        posicao_do_mouse[1]
                        - pos_superior_esquerdo_considerando_borda[1],
                    )
                    pos_no_tabuleiro = (
                        math.floor(
                            pos_mouse_no_tabuleiro_considerando_borda[0]
                            / lado_quadrados[0]
                        ),
                        math.floor(
                            pos_mouse_no_tabuleiro_considerando_borda[1]
                            / lado_quadrados[1]
                        ),
                    )

                    print(f"posicao_do_mouse={posicao_do_mouse}")
                    print(f"pos_no_tabuleiro={pos_no_tabuleiro}")

                    linha = pos_no_tabuleiro[1]
                    coluna = pos_no_tabuleiro[0]

                    if estado_do_tabuleiro[linha][coluna] == "vazio":
                        estado_do_tabuleiro[linha][coluna] = "azul"
                        peca_do_tabuleiro = pygame_gui.elements.UIImage(
                            relative_rect=pygame.Rect(
                                (
                                    (coluna * lado_quadrados[0])
                                    + tamanho_offset_borda_interna[0]
                                    + tamanho_offset_borda_externa[0],
                                    (linha * lado_quadrados[1])
                                    + tamanho_offset_borda_interna[0]
                                    + tamanho_offset_borda_externa[0],
                                ),
                                (
                                    imagem_da_peca_jogador_azul.get_width(),
                                    imagem_da_peca_jogador_azul.get_height(),
                                ),
                            ),
                            image_surface=imagem_da_peca_jogador_azul,
                            manager=gerenciador_interface_grafica,
                            container=interface_do_tabuleiro,
                        )
                        pecas.append(peca_do_tabuleiro)
                    elif estado_do_tabuleiro[linha][coluna] == "azul":
                        estado_do_tabuleiro[linha][coluna] = "vazio"
                        for indice, peca in enumerate(pecas):
                            if peca.rect.collidepoint(posicao_do_mouse):
                                peca.kill()
                                del pecas[indice]

            gerenciador_interface_grafica.process_events(event)

        gerenciador_interface_grafica.update(pygame.time.get_ticks() / 1000)

        janela.fill((255, 255, 255))
        gerenciador_interface_grafica.draw_ui(janela)

        retrato_jogador_com_turno_ativo = (
            retrato_jogador_azul
            if turno_do_jogador == "azul"
            else retrato_jogador_vermelho
        )
        janela.blit(
            imagem_borda_status_turno,
            (
                retrato_jogador_com_turno_ativo.rect.left - 5,
                retrato_jogador_com_turno_ativo.rect.top - 5,
            ),
        )

        pygame.display.update()
