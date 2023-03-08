from typing import Callable, Optional

from gekitai.rede.servicos_de_rede import (
    ServicoDeRede,
)


class ControladorDeRede:
    def __init__(
        self,
        servico_de_rede: ServicoDeRede,
        ao_receber_mensagem: Callable,
        ao_conectar: Optional[Callable] = None,
    ):
        self.servico_de_rede: ServicoDeRede = servico_de_rede
        self.ao_receber_mensagem: Callable = ao_receber_mensagem
        self.ao_conectar: Optional[Callable] = ao_conectar

    def iniciar(self):
        self.servico_de_rede.iniciar(self.ao_receber_mensagem, self.ao_conectar)

    def enviar_mensagem(self, mensagem: str):
        self.servico_de_rede.enviar_mensagem(mensagem)

    def encerrar(self):
        self.servico_de_rede.encerrar()
