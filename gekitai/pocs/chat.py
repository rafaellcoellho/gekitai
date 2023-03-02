import selectors
import socket
import threading
import pygame
import pygame_gui

COR_BRANCO = (255, 255, 255)
COR_PRETO = (0, 0, 0)

LARGURA_DA_JANELA = 600
ALTURA_DA_JANELA = 400


def modo_exemplo_chat_servidor(porta):
    print(f"servidor escutando na porta {porta}")

    pygame.init()

    janela = pygame.display.set_mode((LARGURA_DA_JANELA, ALTURA_DA_JANELA))
    interface_do_chat = pygame_gui.UIManager((LARGURA_DA_JANELA, ALTURA_DA_JANELA))

    entrada_de_texto = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(50, 350, 400, 25),
        manager=interface_do_chat,
    )
    botao_de_enviar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(460, 350, 80, 25),
        text="Enviar",
        manager=interface_do_chat,
    )
    log_de_mensagens = pygame_gui.elements.UITextBox(
        html_text="",
        relative_rect=pygame.Rect(50, 50, 490, 275),
        manager=interface_do_chat,
    )

    seletores = selectors.DefaultSelector()

    socket_do_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_do_servidor.setblocking(False)
    socket_do_servidor.bind(("127.0.0.1", int(porta)))
    socket_do_servidor.listen(1)

    sockets_conectados = []

    def recebe_dados_do_cliente(file_descriptor_socket_cliente):
        dados_recebidos_pela_rede = file_descriptor_socket_cliente.recv(1024)

        if dados_recebidos_pela_rede:
            mensagem_recebida = dados_recebidos_pela_rede.decode("utf-8")
            log_de_mensagens.append_html_text(
                f'<font color="blue">cliente:</font> {mensagem_recebida}<br>'
            )
        else:
            seletores.unregister(file_descriptor_socket_cliente)
            file_descriptor_socket_cliente.close()
            sockets_conectados.clear()

    def inicia_conexao_com_cliente(file_descriptor_socket_servidor):
        socket_do_cliente_conectado, _ = file_descriptor_socket_servidor.accept()
        socket_do_cliente_conectado.setblocking(False)

        sockets_conectados.append(socket_do_cliente_conectado)

        socket_do_cliente_conectado.sendall(b"Conectado")
        seletores.register(
            socket_do_cliente_conectado,
            selectors.EVENT_READ,
            data=recebe_dados_do_cliente,
        )

    seletores.register(
        socket_do_servidor, selectors.EVENT_READ, data=inicia_conexao_com_cliente
    )

    def loop_escutando_mensagens_dos_seletores():
        try:
            while True:
                eventos = seletores.select()
                for key, _ in eventos:
                    funcao_para_tratar_evento = key.data
                    funcao_para_tratar_evento(key.fileobj)
        except KeyboardInterrupt:
            socket_do_servidor.close()
            seletores.close()
            sockets_conectados.clear()

    thread_escutando_mensagens_dos_seletores = threading.Thread(
        target=loop_escutando_mensagens_dos_seletores, daemon=True
    )
    thread_escutando_mensagens_dos_seletores.start()

    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.USEREVENT:
                if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if evento.ui_element == botao_de_enviar:
                        mensagem_para_enviar = entrada_de_texto.get_text()
                        if mensagem_para_enviar:
                            entrada_de_texto.set_text("")
                            log_de_mensagens.append_html_text(
                                f'<font color="black">servidor:</font> {mensagem_para_enviar}<br>'
                            )
                            sockets_conectados[0].sendall(
                                str.encode(f"{mensagem_para_enviar}")
                            )

            interface_do_chat.process_events(evento)

        interface_do_chat.update(clock.tick(60) / 1000.0)

        janela.fill(COR_BRANCO)
        interface_do_chat.draw_ui(janela)
        pygame.display.update()


def modo_exemplo_chat_cliente(ip, porta):
    print(f"conectando no servidor no endereço {ip} na porta {porta}")

    pygame.init()

    janela = pygame.display.set_mode((LARGURA_DA_JANELA, ALTURA_DA_JANELA))
    interface_do_chat = pygame_gui.UIManager((LARGURA_DA_JANELA, ALTURA_DA_JANELA))

    entrada_de_texto = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(50, 350, 400, 25),
        manager=interface_do_chat,
    )
    botao_de_enviar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(460, 350, 80, 25),
        text="Enviar",
        manager=interface_do_chat,
    )
    log_de_mensagens = pygame_gui.elements.UITextBox(
        html_text="",
        relative_rect=pygame.Rect(50, 50, 490, 275),
        manager=interface_do_chat,
    )

    seletores = selectors.DefaultSelector()
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        socket_cliente.connect((ip, int(porta)))

        dados_recebidos_pela_rede = socket_cliente.recv(1024)
        mensagem_recebida = dados_recebidos_pela_rede.decode("utf-8")
        log_de_mensagens.append_html_text(
            f'<font color="black">servidor:</font> {mensagem_recebida}<br>'
        )

        socket_cliente.setblocking(False)
    except OSError as msg:
        socket_cliente.close()
        return

    def recebe_dados_do_servidor(file_descriptor_socket_cliente):
        dados_recebidos_pela_rede_do_servidor = file_descriptor_socket_cliente.recv(
            1024
        )

        if dados_recebidos_pela_rede_do_servidor:
            mensagem_recebida_do_servidor = (
                dados_recebidos_pela_rede_do_servidor.decode("utf-8")
            )
            log_de_mensagens.append_html_text(
                f'<font color="black">servidor:</font> {mensagem_recebida_do_servidor}<br>'
            )
        else:
            seletores.unregister(file_descriptor_socket_cliente)
            file_descriptor_socket_cliente.close()

    seletores.register(
        socket_cliente, selectors.EVENT_READ, data=recebe_dados_do_servidor
    )

    def loop_escutando_mensagens_dos_seletores():
        try:
            while True:
                eventos = seletores.select()
                for key, _ in eventos:
                    funcao_para_tratar_evento = key.data
                    funcao_para_tratar_evento(key.fileobj)
        except KeyboardInterrupt:
            socket_cliente.close()
            seletores.close()

    thread_escutando_mensagens_dos_seletores = threading.Thread(
        target=loop_escutando_mensagens_dos_seletores, daemon=True
    )
    thread_escutando_mensagens_dos_seletores.start()

    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.USEREVENT:
                if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if evento.ui_element == botao_de_enviar:
                        mensagem_para_enviar = entrada_de_texto.get_text()
                        if mensagem_para_enviar:
                            entrada_de_texto.set_text("")
                            log_de_mensagens.append_html_text(
                                f'<font color="blue">cliente:</font> {mensagem_para_enviar}<br>'
                            )
                            socket_cliente.send(str.encode(f"{mensagem_para_enviar}"))

            interface_do_chat.process_events(evento)

        interface_do_chat.update(clock.tick(60) / 1000.0)

        janela.fill(COR_BRANCO)
        interface_do_chat.draw_ui(janela)
        pygame.display.update()
