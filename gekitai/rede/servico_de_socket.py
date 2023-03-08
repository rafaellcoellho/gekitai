from selectors import DefaultSelector, EVENT_READ
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from typing import Optional, Callable

from gekitai.rede.servicos_de_rede import (
    ServicoDeRede,
    InformacaoDeConexao,
    FuncaoExecutadaAoReceberMensagem,
)


class ServicoDeSocket(ServicoDeRede):
    def __init__(
        self,
        info_de_conexao: InformacaoDeConexao,
        eh_anfitriao: bool,
    ):
        super().__init__(info_de_conexao, eh_anfitriao)
        self.seletores: DefaultSelector = DefaultSelector()
        self.socket: socket = socket(AF_INET, SOCK_STREAM)
        self.socket_conectado_ao_cliente: Optional[socket] = None
        self.ao_receber_mensagem: Optional[FuncaoExecutadaAoReceberMensagem] = None

    def iniciar(self, ao_receber_mensagem: FuncaoExecutadaAoReceberMensagem):
        self.ao_receber_mensagem = ao_receber_mensagem

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

    def enviar_mensagem(self, mensagem: str):
        bytes_para_enviar: bytes = str.encode(mensagem)
        if self.eh_anfitriao and self.socket_conectado_ao_cliente:
            self.socket_conectado_ao_cliente.sendall(bytes_para_enviar)
        else:
            self.socket.send(bytes_para_enviar)

    def encerrar(self):
        if self.socket_conectado_ao_cliente:
            self.socket_conectado_ao_cliente.close()
        self.socket.close()
        self.seletores.close()

    def _ao_iniciar_conexao_com_cliente(self, socket_servidor: socket):
        self.socket_conectado_ao_cliente, _ = socket_servidor.accept()
        self.socket_conectado_ao_cliente.setblocking(False)
        self.seletores.register(
            self.socket_conectado_ao_cliente,
            EVENT_READ,
            data=self._ao_receber_dados,
        )

    def _ao_receber_dados(self, socket_cliente):
        dados_recebidos: bytes = socket_cliente.recv(1024)
        if dados_recebidos:
            mensagem_recebida = dados_recebidos.decode("utf-8")
            self.ao_receber_mensagem(mensagem=mensagem_recebida)
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
