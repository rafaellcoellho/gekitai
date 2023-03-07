import math
import re
import selectors
import socket
import threading

import pygame
import pygame_gui


def main(papel, ip, porta):
    # constantes
    tamanho_da_janela = (936, 655)
    cor_de_fundo = (255, 255, 255)

    identificacao_do_servidor_no_chat = "<font color=#46B8F7>servidor</font>"
    identificacao_do_cliente_no_chat = "<font color=#C65454>cliente</font>"

    parser_do_comando_criar_peca = re.compile(r"^CNP=\((\d), (\d), (\d)\)$")
    parser_do_comando_remover_peca = re.compile(r"^RPE=\((\d), (\d), (\d+), (\d+)\)$")
    parser_do_comando_mensagem_do_chat = re.compile(r"^CHT=(.*)$")

    tamanho_offset_borda_externa = (11, 11)
    tamanho_offset_borda_interna = (10, 10)
    lado_quadrados = (87, 87)

    pos_superior_esquerdo_interface_de_jogo = (10, 10)
    pos_superior_esquerdo_considerando_borda = (
        pos_superior_esquerdo_interface_de_jogo[0]
        + tamanho_offset_borda_externa[0]
        + tamanho_offset_borda_interna[0]
    ), (
        pos_superior_esquerdo_interface_de_jogo[1]
        + tamanho_offset_borda_externa[1]
        + tamanho_offset_borda_interna[1]
    )
    pos_inferior_direito_considerando_borda = (
        pos_superior_esquerdo_considerando_borda[0] + (6 * lado_quadrados[0]),
        pos_superior_esquerdo_considerando_borda[1] + (6 * lado_quadrados[1]),
    )

    # estado inicial do jogo
    estado_do_jogo = {
        "ganhador": "nenhum",
        "executando": True,
        "turno_do_jogador": "servidor",
        "estado_do_tabuleiro": [
            ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
            ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
            ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
            ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
            ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
            ["vazio", "vazio", "vazio", "vazio", "vazio", "vazio"],
        ],
    }
    interface_grafica_das_pecas_no_tabuleiro = []

    # carregando assets
    imagem_do_tabuleiro = pygame.image.load("assets/tabuleiro.png")
    imagem_do_retrato_jogador_servidor = pygame.transform.smoothscale(
        pygame.image.load("assets/retrato_jogador_azul.png"), (54, 69)
    )
    imagem_do_retrato_jogador_cliente = pygame.transform.smoothscale(
        pygame.image.load("assets/retrato_jogador_vermelho.png"), (54, 69)
    )
    imagem_da_peca_jogador_servidor = pygame.transform.smoothscale(
        pygame.image.load("assets/peca_jogador_azul.png"), (80, 80)
    )
    imagem_da_peca_jogador_cliente = pygame.transform.smoothscale(
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
                imagem_do_retrato_jogador_servidor.get_height(),
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
    retrato_jogador_servidor = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (0, 0),
            (
                imagem_do_retrato_jogador_servidor.get_width(),
                imagem_do_retrato_jogador_servidor.get_height(),
            ),
        ),
        image_surface=imagem_do_retrato_jogador_servidor,
        manager=gerenciador_de_interface_grafica,
        container=interface_de_status_do_turno,
    )
    retrato_jogador_cliente = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect(
            (10, 0),
            (
                imagem_do_retrato_jogador_cliente.get_width(),
                imagem_do_retrato_jogador_cliente.get_height(),
            ),
        ),
        image_surface=imagem_do_retrato_jogador_cliente,
        manager=gerenciador_de_interface_grafica,
        container=interface_de_status_do_turno,
        anchors={"left": "left", "left_target": retrato_jogador_servidor},
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

    def inserir_peca_no_tabuleiro(linha_alvo, coluna_alvo, peca_alvo):
        estado_do_jogo["estado_do_tabuleiro"][linha_alvo][coluna_alvo] = peca_alvo
        imagem_da_peca_por_papel = (
            imagem_da_peca_jogador_servidor
            if peca_alvo == "servidor"
            else imagem_da_peca_jogador_cliente
        )
        peca_do_tabuleiro = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                (
                    (coluna_alvo * lado_quadrados[0])
                    + tamanho_offset_borda_interna[0]
                    + tamanho_offset_borda_externa[0],
                    (linha_alvo * lado_quadrados[1])
                    + tamanho_offset_borda_interna[0]
                    + tamanho_offset_borda_externa[0],
                ),
                (
                    imagem_da_peca_por_papel.get_width(),
                    imagem_da_peca_por_papel.get_height(),
                ),
            ),
            image_surface=imagem_da_peca_por_papel,
            manager=gerenciador_de_interface_grafica,
            container=interface_do_tabuleiro,
        )
        interface_grafica_das_pecas_no_tabuleiro.append(peca_do_tabuleiro)

    def remover_peca_no_tabuleiro(linha_alvo, coluna_alvo, ponto_do_clique):
        estado_do_jogo["estado_do_tabuleiro"][linha_alvo][coluna_alvo] = "vazio"
        for indice, peca in enumerate(interface_grafica_das_pecas_no_tabuleiro):
            if peca.rect.collidepoint(ponto_do_clique):
                peca.kill()
                del interface_grafica_das_pecas_no_tabuleiro[indice]

    # inicia interface de rede
    seletores = selectors.DefaultSelector()
    sockets_conectados = []

    instancia_do_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if papel == "servidor":
        instancia_do_socket.setblocking(False)
        instancia_do_socket.bind(("127.0.0.1", int(porta)))
        instancia_do_socket.listen(1)

        def recebe_dados_do_cliente(file_descriptor_socket_cliente):
            dados_recebidos_pela_rede = file_descriptor_socket_cliente.recv(1024)

            if dados_recebidos_pela_rede:
                mensagem_recebida = dados_recebidos_pela_rede.decode("utf-8")
                if mensagem_recebida == "DST":
                    estado_do_jogo["ganhador"] = "servidor"
                    estado_do_jogo["executando"] = False
                elif mensagem_recebida == "PAS":
                    estado_do_jogo["turno_do_jogador"] = "servidor"
                elif parser_do_comando_criar_peca.match(mensagem_recebida):
                    inserir_peca_no_tabuleiro(
                        linha_alvo=int(mensagem_recebida[8]),
                        coluna_alvo=int(mensagem_recebida[5]),
                        peca_alvo="servidor"
                        if int(mensagem_recebida[11]) == 0
                        else "cliente",
                    )
                elif parser_do_comando_remover_peca.match(mensagem_recebida):
                    (
                        linha_alvo,
                        coluna_alvo,
                        posicao_do_mouse_x,
                        posicao_do_mouse_y,
                    ) = parser_do_comando_remover_peca.match(mensagem_recebida).group(
                        1, 2, 3, 4
                    )
                    remover_peca_no_tabuleiro(
                        linha_alvo=int(linha_alvo),
                        coluna_alvo=int(coluna_alvo),
                        ponto_do_clique=(
                            int(posicao_do_mouse_x),
                            int(posicao_do_mouse_y),
                        ),
                    )
                elif parser_do_comando_mensagem_do_chat.match(mensagem_recebida):
                    conteudo = mensagem_recebida[4:]
                    log_de_mensagens.append_html_text(
                        f"{identificacao_do_cliente_no_chat}: {conteudo}<br>"
                    )
            else:
                seletores.unregister(file_descriptor_socket_cliente)
                file_descriptor_socket_cliente.close()
                sockets_conectados.clear()

        def inicia_conexao_com_cliente(file_descriptor_socket_servidor):
            socket_do_cliente_conectado, _ = file_descriptor_socket_servidor.accept()
            socket_do_cliente_conectado.setblocking(False)

            sockets_conectados.append(socket_do_cliente_conectado)

            seletores.register(
                socket_do_cliente_conectado,
                selectors.EVENT_READ,
                data=recebe_dados_do_cliente,
            )

        seletores.register(
            instancia_do_socket, selectors.EVENT_READ, data=inicia_conexao_com_cliente
        )
    elif papel == "cliente":
        try:
            instancia_do_socket.connect((ip, int(porta)))
            instancia_do_socket.setblocking(False)
        except OSError as msg:
            instancia_do_socket.close()
            print(msg)
            return

        def recebe_dados_do_servidor(file_descriptor_socket_cliente):
            dados_recebidos_pela_rede_do_servidor = file_descriptor_socket_cliente.recv(
                1024
            )

            if dados_recebidos_pela_rede_do_servidor:
                mensagem_recebida_do_servidor = (
                    dados_recebidos_pela_rede_do_servidor.decode("utf-8")
                )
                if mensagem_recebida_do_servidor == "DST":
                    estado_do_jogo["ganhador"] = "cliente"
                    estado_do_jogo["executando"] = False
                elif mensagem_recebida_do_servidor == "PAS":
                    estado_do_jogo["turno_do_jogador"] = "cliente"
                elif parser_do_comando_criar_peca.match(mensagem_recebida_do_servidor):
                    inserir_peca_no_tabuleiro(
                        linha_alvo=int(mensagem_recebida_do_servidor[8]),
                        coluna_alvo=int(mensagem_recebida_do_servidor[5]),
                        peca_alvo="servidor"
                        if int(mensagem_recebida_do_servidor[11]) == 0
                        else "cliente",
                    )
                elif parser_do_comando_remover_peca.match(
                    mensagem_recebida_do_servidor
                ):
                    (
                        linha_alvo,
                        coluna_alvo,
                        posicao_do_mouse_x,
                        posicao_do_mouse_y,
                    ) = parser_do_comando_remover_peca.match(
                        mensagem_recebida_do_servidor
                    ).group(
                        1, 2, 3, 4
                    )
                    remover_peca_no_tabuleiro(
                        linha_alvo=int(linha_alvo),
                        coluna_alvo=int(coluna_alvo),
                        ponto_do_clique=(
                            int(posicao_do_mouse_x),
                            int(posicao_do_mouse_y),
                        ),
                    )
                elif parser_do_comando_mensagem_do_chat.match(
                    mensagem_recebida_do_servidor
                ):
                    conteudo = mensagem_recebida_do_servidor[4:]
                    log_de_mensagens.append_html_text(
                        f"{identificacao_do_servidor_no_chat}: {conteudo}<br>"
                    )
            else:
                seletores.unregister(file_descriptor_socket_cliente)
                file_descriptor_socket_cliente.close()

        seletores.register(
            instancia_do_socket, selectors.EVENT_READ, data=recebe_dados_do_servidor
        )
    else:
        print("papel na rede invalido")
        return

    def envia_mensagem_para_jogador_oponente(mensagem):
        if papel == "servidor":
            sockets_conectados[0].sendall(str.encode(f"{mensagem}"))
        elif papel == "cliente":
            instancia_do_socket.send(str.encode(f"{mensagem}"))
        else:
            print("papel na rede invalido")
            return

    # inicia thread escutando por mensagens da rede
    def loop_escutando_mensagens_dos_seletores():
        try:
            while True:
                eventos = seletores.select()
                for key, _ in eventos:
                    funcao_para_tratar_evento = key.data
                    funcao_para_tratar_evento(key.fileobj)
        except KeyboardInterrupt:
            instancia_do_socket.close()
            seletores.close()
            sockets_conectados.clear()

    thread_escutando_mensagens_dos_seletores = threading.Thread(
        target=loop_escutando_mensagens_dos_seletores, daemon=True
    )
    thread_escutando_mensagens_dos_seletores.start()

    # relogio do jogo
    relogio = pygame.time.Clock()

    while estado_do_jogo["executando"]:
        delta_de_tempo = relogio.tick(60)

        # processar input de usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado_do_jogo["executando"] = False
            elif evento.type == pygame.USEREVENT:
                if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if evento.ui_element == botao_de_desistir:
                        envia_mensagem_para_jogador_oponente(f"DST")
                        estado_do_jogo["ganhador"] = (
                            "servidor" if papel == "cliente" else "cliente"
                        )
                        estado_do_jogo["executando"] = False
                    elif evento.ui_element == botao_de_passar_turno:
                        if (
                            papel == "servidor"
                            and estado_do_jogo["turno_do_jogador"] == "servidor"
                        ):
                            envia_mensagem_para_jogador_oponente(f"PAS")
                            estado_do_jogo["turno_do_jogador"] = "cliente"
                        elif (
                            papel == "cliente"
                            and estado_do_jogo["turno_do_jogador"] == "cliente"
                        ):
                            envia_mensagem_para_jogador_oponente(f"PAS")
                            estado_do_jogo["turno_do_jogador"] = "servidor"
                    elif evento.ui_element == botao_de_enviar:
                        mensagem_para_enviar = entrada_de_texto.get_text()
                        if mensagem_para_enviar:
                            entrada_de_texto.set_text("")
                            identificacao_jogador_no_chat = (
                                identificacao_do_servidor_no_chat
                                if papel == "servidor"
                                else identificacao_do_cliente_no_chat
                            )
                            log_de_mensagens.append_html_text(
                                f"{identificacao_jogador_no_chat}: {mensagem_para_enviar}<br>"
                            )
                            envia_mensagem_para_jogador_oponente(
                                f"CHT={mensagem_para_enviar}"
                            )
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if estado_do_jogo["turno_do_jogador"] == papel:
                    posicao_do_mouse = pygame.mouse.get_pos()

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

                        linha = pos_no_tabuleiro[1]
                        coluna = pos_no_tabuleiro[0]

                        if (
                            estado_do_jogo["estado_do_tabuleiro"][linha][coluna]
                            == "vazio"
                        ):
                            jogador = papel
                            oponente = "cliente" if papel == "servidor" else "servidor"
                            peca_que_vai_interagir = (
                                jogador if evento.button == 1 else oponente
                            )
                            inserir_peca_no_tabuleiro(
                                linha, coluna, peca_que_vai_interagir
                            )
                            if jogador == "servidor":
                                peca_que_oponente_tem_que_colocar = (
                                    0 if evento.button == 1 else 1
                                )
                            else:
                                peca_que_oponente_tem_que_colocar = (
                                    1 if evento.button == 1 else 0
                                )
                            envia_mensagem_para_jogador_oponente(
                                f"CNP=({coluna}, {linha}, {peca_que_oponente_tem_que_colocar})"
                            )
                        else:
                            remover_peca_no_tabuleiro(linha, coluna, posicao_do_mouse)
                            envia_mensagem_para_jogador_oponente(
                                f"RPE=({coluna}, {linha}, {posicao_do_mouse[0]}, {posicao_do_mouse[1]})"
                            )

            gerenciador_de_interface_grafica.process_events(evento)

        # atualizar estado do jogo
        gerenciador_de_interface_grafica.update(delta_de_tempo / 1000.0)

        retrato_jogador_com_turno_ativo = (
            retrato_jogador_servidor
            if estado_do_jogo["turno_do_jogador"] == "servidor"
            else retrato_jogador_cliente
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

    print(f"Parabéns ao ganhador do jogo: {estado_do_jogo['ganhador']}")
    pygame.quit()