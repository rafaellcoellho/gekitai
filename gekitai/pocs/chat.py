import selectors
import socket
import threading


def modo_exemplo_chat_servidor(porta):
    print(f"servidor escutando na porta {porta}")

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
            print(f"\ncliente: {mensagem_recebida}")
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

    while True:
        mensagem = input("mensagem para enviar: ")
        if len(sockets_conectados) > 0:
            sockets_conectados[0].sendall(str.encode(f"{mensagem}"))
        else:
            print("ainda não tem nenhum cliente conectado!")


def modo_exemplo_chat_cliente(ip, porta):
    print(f"conectando no servidor no endereço {ip} na porta {porta}")

    seletores = selectors.DefaultSelector()

    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        socket_cliente.connect((ip, int(porta)))

        dados_recebidos_pela_rede = socket_cliente.recv(1024)
        mensagem_recebida = dados_recebidos_pela_rede.decode("utf-8")
        print(f"\nservidor: {mensagem_recebida}")

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
            print(f"\nservidor: {mensagem_recebida_do_servidor}")
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

    while True:
        mensagem = input("mensagem para enviar: ")
        socket_cliente.send(str.encode(f"{mensagem}"))
