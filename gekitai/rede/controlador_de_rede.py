from gekitai.rede.servicos_de_rede import (
    ServicoDeRede,
    FuncaoExecutadaAoReceberMensagem,
)


class ControladorDeRede:
    def __init__(
        self,
        servico_de_rede: ServicoDeRede,
        ao_receber_mensagem: FuncaoExecutadaAoReceberMensagem,
    ):
        self.servico_de_rede: ServicoDeRede = servico_de_rede
        self.ao_receber_mensagem: FuncaoExecutadaAoReceberMensagem = ao_receber_mensagem

    def iniciar(self):
        self.servico_de_rede.iniciar(self.ao_receber_mensagem)

    def enviar_mensagem(self, mensagem: str):
        self.servico_de_rede.enviar_mensagem(mensagem)

    def encerrar(self):
        self.servico_de_rede.encerrar()
