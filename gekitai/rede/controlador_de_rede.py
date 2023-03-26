from gekitai.rede.servicos_de_rede import (
    ServicoDeRede,
)


class ControladorDeRede:
    def __init__(
        self,
        servico_de_rede: ServicoDeRede,
    ):
        self.servico_de_rede: ServicoDeRede = servico_de_rede
        self.servico_de_rede.iniciar()

    def informar_desistencia(self):
        if self.servico_de_rede.controlador_oponente:
            self.servico_de_rede.garantir_funcionamento_do_servico_de_rede()
            self.servico_de_rede.controlador_oponente.informar_desistencia()

    def passar_turno(self):
        if self.servico_de_rede.controlador_oponente:
            self.servico_de_rede.garantir_funcionamento_do_servico_de_rede()
            self.servico_de_rede.controlador_oponente.passar_turno()

    def adicionar_mensagem_no_chat(self, mensagem: str):
        if self.servico_de_rede.controlador_oponente:
            self.servico_de_rede.garantir_funcionamento_do_servico_de_rede()
            self.servico_de_rede.controlador_oponente.adicionar_mensagem_no_chat(
                mensagem
            )

    def criar_peca_no_tabuleiro(self, peca: int, linha: int, coluna: int):
        if self.servico_de_rede.controlador_oponente:
            self.servico_de_rede.garantir_funcionamento_do_servico_de_rede()
            self.servico_de_rede.controlador_oponente.criar_peca_no_tabuleiro(
                peca, linha, coluna
            )

    def remover_peca_do_tabuleiro(
        self, linha: int, coluna: int, posicao_x_mouse: int, posicao_y_mouse: int
    ):
        if self.servico_de_rede.controlador_oponente:
            self.servico_de_rede.garantir_funcionamento_do_servico_de_rede()
            self.servico_de_rede.controlador_oponente.remover_peca_do_tabuleiro(
                linha, coluna, posicao_x_mouse, posicao_y_mouse
            )

    def encerrar(self):
        self.servico_de_rede.encerrar()
