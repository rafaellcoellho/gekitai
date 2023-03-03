import pygame
import pygame_gui


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

    tamanho_da_janela = (575, 650)
    janela = pygame.display.set_mode(tamanho_da_janela)
    janela.fill((255, 255, 255))

    interface_do_jogo = pygame_gui.UIManager(tamanho_da_janela)

    tabuleiro = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (10, 10),
            (imagem_do_tabuleiro.get_width(), imagem_do_tabuleiro.get_height()),
        ),
        image_surface=imagem_do_tabuleiro,
        manager=interface_do_jogo,
    )
    botao_de_desistir = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((367, 570), (100, 69)),
        text="Desistir",
        manager=interface_do_jogo,
    )
    botao_de_passar_turno = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((467, 570), (100, 69)),
        text="Passar",
        manager=interface_do_jogo,
    )
    retrato_jogador_azul = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (20, 570),
            (
                imagem_do_retrato_jogador_azul.get_width(),
                imagem_do_retrato_jogador_azul.get_height(),
            ),
        ),
        image_surface=imagem_do_retrato_jogador_azul,
        manager=interface_do_jogo,
    )
    retrato_jogador_vermelho = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (104, 570),
            (
                imagem_do_retrato_jogador_vermelho.get_width(),
                imagem_do_retrato_jogador_vermelho.get_height(),
            ),
        ),
        image_surface=imagem_do_retrato_jogador_vermelho,
        manager=interface_do_jogo,
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
                board_pos = (
                    posicao_do_mouse[0] - tabuleiro.rect.x,
                    posicao_do_mouse[1] - tabuleiro.rect.y,
                )

                linha = board_pos[1] // 100
                coluna = board_pos[0] // 100

                if estado_do_tabuleiro[linha][coluna] == "vazio":
                    estado_do_tabuleiro[linha][coluna] = "azul"
                    pygame_gui.elements.UIImage(
                        relative_rect=pygame.Rect(
                            ((coluna * 100) + 33, (linha * 100) + 30),
                            (
                                imagem_da_peca_jogador_azul.get_width(),
                                imagem_da_peca_jogador_azul.get_height(),
                            ),
                        ),
                        image_surface=imagem_da_peca_jogador_azul,
                        manager=tabuleiro.ui_manager,
                    )
                elif estado_do_tabuleiro[linha][coluna] == "azul":
                    estado_do_tabuleiro[linha][coluna] = "vazio"
                    for elemento_da_interface in tabuleiro.ui_manager:
                        if isinstance(
                            elemento_da_interface, pygame_gui.elements.UIImage
                        ):
                            if elemento_da_interface.rect.collidepoint(
                                posicao_do_mouse
                            ):
                                elemento_da_interface.kill()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                posicao_do_mouse = pygame.mouse.get_pos()
                board_pos = (
                    posicao_do_mouse[0] - tabuleiro.rect.x,
                    posicao_do_mouse[1] - tabuleiro.rect.y,
                )

                linha = board_pos[1] // 100
                coluna = board_pos[0] // 100

                if estado_do_tabuleiro[linha][coluna] == "vazio":
                    estado_do_tabuleiro[linha][coluna] = "vermelho"
                    pygame_gui.elements.UIImage(
                        relative_rect=pygame.Rect(
                            ((coluna * 100) + 50, (linha * 100) + 50),
                            (
                                imagem_da_peca_jogador_vermelho.get_width(),
                                imagem_da_peca_jogador_vermelho.get_height(),
                            ),
                        ),
                        image_surface=imagem_da_peca_jogador_vermelho,
                        manager=tabuleiro.ui_manager,
                    )
                elif estado_do_tabuleiro[linha][coluna] == "vermelho":
                    estado_do_tabuleiro[linha][coluna] = "vazio"
                    for elemento_da_interface in tabuleiro.ui_manager:
                        if isinstance(
                            elemento_da_interface, pygame_gui.elements.UIImage
                        ):
                            if elemento_da_interface.rect.collidepoint(
                                posicao_do_mouse
                            ):
                                elemento_da_interface.kill()

            interface_do_jogo.process_events(event)

        interface_do_jogo.update(pygame.time.get_ticks() / 1000)

        janela.fill((255, 255, 255))
        interface_do_jogo.draw_ui(janela)

        padding = 3
        retrato_jogador_com_turno_ativo = (
            retrato_jogador_azul
            if turno_do_jogador == "azul"
            else retrato_jogador_vermelho
        )
        pygame.draw.rect(
            janela,
            (255, 0, 0),
            pygame.Rect(
                retrato_jogador_com_turno_ativo.rect.left - padding,
                retrato_jogador_com_turno_ativo.rect.top - padding,
                retrato_jogador_com_turno_ativo.rect.width + 2 * padding,
                retrato_jogador_com_turno_ativo.rect.height + 2 * padding,
            ),
            width=2,
        )

        pygame.display.flip()
