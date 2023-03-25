import re
from selectors import DefaultSelector, EVENT_READ
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from typing import Optional, Callable, Any

from gekitai.rede.servicos_de_rede import (
    ServicoDeRede,
    InformacaoDeConexao,
    ControladorDeOponente,
)


class ControladorDeOponenteSocket(ControladorDeOponente):
    def __init__(self, servico_de_socket: "ServicoDeSocket"):
        self.servico_de_socket = servico_de_socket

    def informar_desistencia(self):
        self.servico_de_socket.enviar_mensagem(f"DST")

    def passar_turno(self):
        self.servico_de_socket.enviar_mensagem(f"PAS")

    def adicionar_mensagem_no_chat(self, mensagem: str):
        self.servico_de_socket.enviar_mensagem(f"CHT={mensagem}")

    def criar_peca_no_tabuleiro(self, peca: int, linha: int, coluna: int):
        self.servico_de_socket.enviar_mensagem(f"CNP=({coluna}, {linha}, {peca})")

    def remover_peca_do_tabuleiro(
        self, linha: int, coluna: int, posicao_x_mouse: int, posicao_y_mouse: int
    ):
        self.servico_de_socket.enviar_mensagem(
            f"RPE=({coluna}, {linha}, {posicao_x_mouse}, {posicao_y_mouse})"
        )


class ServicoDeSocket(ServicoDeRede):
    def __init__(
        self,
        info_de_conexao: InformacaoDeConexao,
        eh_anfitriao: bool,
        controlador_local: Any,
    ):
        super().__init__(
            info_de_conexao, eh_anfitriao, controlador_local=controlador_local
        )

        self.seletores: DefaultSelector = DefaultSelector()
        self.socket: socket = socket(AF_INET, SOCK_STREAM)
        self.socket_conectado_ao_cliente: Optional[socket] = None

        self.parser_do_comando_criar_peca = re.compile(r"^CNP=\((\d), (\d), (\d)\)$")
        self.parser_do_comando_remover_peca = re.compile(
            r"^RPE=\((\d), (\d), (\d+), (\d+)\)$"
        )
        self.parser_do_comando_mensagem_do_chat = re.compile(r"^CHT=(.*)$")

        self.controlador_oponente = ControladorDeOponenteSocket(servico_de_socket=self)

    def iniciar(self):
        if self.eh_anfitriao:
            self.socket.setblocking(False)
            self.socket.bind(
                (self.info_de_conexao.endereco, self.info_de_conexao.porta)
            )
            self.socket.listen(1)

            self.seletores.register(
                self.socket,
                EVENT_READ,
                data=self._ao_iniciar_conexao_com_cliente,
            )
        else:
            self.socket.connect(
                (self.info_de_conexao.endereco, self.info_de_conexao.porta)
            )
            self.socket.setblocking(False)
            self.seletores.register(
                self.socket,
                EVENT_READ,
                data=self._ao_receber_dados,
            )

        thread_escutando_mensagens_dos_seletores: Thread = Thread(
            target=self._loop_escutando_seletores,
            daemon=True,
        )
        thread_escutando_mensagens_dos_seletores.start()

    def encerrar(self):
        if self.socket_conectado_ao_cliente:
            self.socket_conectado_ao_cliente.close()
        self.socket.close()
        self.seletores.close()

    def enviar_mensagem(self, mensagem: str):
        bytes_para_enviar: bytes = str.encode(mensagem)
        if self.eh_anfitriao and self.socket_conectado_ao_cliente:
            self.socket_conectado_ao_cliente.sendall(bytes_para_enviar)
        else:
            self.socket.send(bytes_para_enviar)

    def _ao_iniciar_conexao_com_cliente(self, socket_servidor: socket):
        self.socket_conectado_ao_cliente, _ = socket_servidor.accept()
        self.socket_conectado_ao_cliente.setblocking(False)
        self.seletores.register(
            self.socket_conectado_ao_cliente,
            EVENT_READ,
            data=self._ao_receber_dados,
        )
        if self.eh_anfitriao:
            self.controlador_local.estado.atualizar_para_tela_de_jogo()

    def _ao_receber_dados(self, socket_cliente):
        dados_recebidos: bytes = socket_cliente.recv(1024)
        if dados_recebidos:
            mensagem_recebida = dados_recebidos.decode("utf-8")
            if self.eh_anfitriao:
                self._ao_receber_mensagem_do_cliente(mensagem_recebida)
            else:
                self._ao_receber_mensagem_do_servidor(mensagem_recebida)
        else:
            self.encerrar()

    def _loop_escutando_seletores(self):
        try:
            while True:
                eventos = self.seletores.select()
                for chave, _ in eventos:
                    funcao_para_reagir_ao_evento: Callable = chave.data
                    socket_alvo = chave.fileobj
                    funcao_para_reagir_ao_evento(socket_alvo)
        except KeyboardInterrupt:
            self.encerrar()

    def _ao_receber_mensagem_do_cliente(self, mensagem_recebida: str):
        if mensagem_recebida == "DST":
            self.controlador_local.estado.define_ganhador_do_jogo("servidor")
        elif mensagem_recebida == "PAS":
            self.controlador_local.estado.define_jogador_que_detem_o_turno("servidor")
        else:
            resultado_match_parser_comando_criar_peca = (
                self.parser_do_comando_criar_peca.match(mensagem_recebida)
            )
            resultado_match_parser_comando_remover_peca = (
                self.parser_do_comando_remover_peca.match(mensagem_recebida)
            )
            resultado_match_parser_comando_mensagem_do_chat = (
                self.parser_do_comando_mensagem_do_chat.match(mensagem_recebida)
            )

            if resultado_match_parser_comando_criar_peca:
                self.controlador_local.tabuleiro.inserir_peca_no_tabuleiro(
                    linha_alvo=int(mensagem_recebida[8]),
                    coluna_alvo=int(mensagem_recebida[5]),
                    peca_alvo="servidor"
                    if int(mensagem_recebida[11]) == 0
                    else "cliente",
                )
            elif resultado_match_parser_comando_remover_peca:
                (
                    linha_alvo,
                    coluna_alvo,
                    posicao_do_mouse_x,
                    posicao_do_mouse_y,
                ) = resultado_match_parser_comando_remover_peca.group(1, 2, 3, 4)
                self.controlador_local.tabuleiro.remover_peca_no_tabuleiro(
                    linha_alvo=int(linha_alvo),
                    coluna_alvo=int(coluna_alvo),
                    ponto_do_clique=(
                        int(posicao_do_mouse_x),
                        int(posicao_do_mouse_y),
                    ),
                )
            elif resultado_match_parser_comando_mensagem_do_chat:
                conteudo = mensagem_recebida[4:]
                self.controlador_local.chat.registrar_mensagem(
                    conteudo, self.controlador_local.chat.identificacao_do_cliente
                )

    def _ao_receber_mensagem_do_servidor(self, mensagem_recebida: str):
        if mensagem_recebida == "DST":
            self.controlador_local.estado.define_ganhador_do_jogo("cliente")
        elif mensagem_recebida == "PAS":
            self.controlador_local.estado.define_jogador_que_detem_o_turno("cliente")
        else:
            resultado_match_parser_comando_criar_peca = (
                self.parser_do_comando_criar_peca.match(mensagem_recebida)
            )
            resultado_match_parser_comando_remover_peca = (
                self.parser_do_comando_remover_peca.match(mensagem_recebida)
            )
            resultado_match_parser_comando_mensagem_do_chat = (
                self.parser_do_comando_mensagem_do_chat.match(mensagem_recebida)
            )

            if resultado_match_parser_comando_criar_peca:
                self.controlador_local.tabuleiro.inserir_peca_no_tabuleiro(
                    linha_alvo=int(mensagem_recebida[8]),
                    coluna_alvo=int(mensagem_recebida[5]),
                    peca_alvo="servidor"
                    if int(mensagem_recebida[11]) == 0
                    else "cliente",
                )
            elif resultado_match_parser_comando_remover_peca:
                (
                    linha_alvo,
                    coluna_alvo,
                    posicao_do_mouse_x,
                    posicao_do_mouse_y,
                ) = resultado_match_parser_comando_remover_peca.group(1, 2, 3, 4)
                self.controlador_local.tabuleiro.remover_peca_no_tabuleiro(
                    linha_alvo=int(linha_alvo),
                    coluna_alvo=int(coluna_alvo),
                    ponto_do_clique=(
                        int(posicao_do_mouse_x),
                        int(posicao_do_mouse_y),
                    ),
                )
            elif resultado_match_parser_comando_mensagem_do_chat:
                conteudo = mensagem_recebida[4:]
                self.controlador_local.chat.registrar_mensagem(
                    conteudo, self.controlador_local.chat.identificacao_do_servidor
                )
