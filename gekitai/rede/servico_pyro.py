import threading
from threading import Thread
from typing import Any

import Pyro5.api

from gekitai.rede.servicos_de_rede import (
    ServicoDeRede,
    InformacaoDeConexao,
    ControladorDeOponente,
)


@Pyro5.api.expose
class ControladorPyro(ControladorDeOponente):
    def __init__(
        self, controlador: Any, eh_anfitriao: bool, funcao_ao_cliente_estar_pronto: Any
    ):
        self.controlador = controlador
        self.eh_anfitriao = eh_anfitriao
        self.funcao_ao_cliente_estar_pronto = funcao_ao_cliente_estar_pronto

    def informar_desistencia(self):
        self.controlador.estado.define_ganhador_do_jogo(
            "servidor" if self.eh_anfitriao else "cliente"
        )

    def passar_turno(self):
        self.controlador.estado.define_jogador_que_detem_o_turno(
            "servidor" if self.eh_anfitriao else "cliente"
        )

    def adicionar_mensagem_no_chat(self, mensagem: str):
        print(self.eh_anfitriao)
        self.controlador.chat.registrar_mensagem(
            mensagem,
            self.controlador.chat.identificacao_do_cliente
            if self.eh_anfitriao
            else self.controlador.chat.identificacao_do_servidor,
        )

    def criar_peca_no_tabuleiro(self, peca: int, linha: int, coluna: int):
        self.controlador.tabuleiro.inserir_peca_no_tabuleiro(
            linha_alvo=int(linha),
            coluna_alvo=int(coluna),
            peca_alvo="servidor" if peca == 0 else "cliente",
        )

    def remover_peca_do_tabuleiro(
        self, linha: int, coluna: int, posicao_x_mouse: int, posicao_y_mouse: int
    ):
        self.controlador.tabuleiro.remover_peca_no_tabuleiro(
            linha_alvo=linha,
            coluna_alvo=coluna,
            ponto_do_clique=(
                posicao_x_mouse,
                posicao_y_mouse,
            ),
        )

    def atualizar_para_tela_de_jogo(self):
        self.controlador.estado.atualizar_para_tela_de_jogo()

    def avisar_servidor_que_cliente_esta_pronto(self):
        self.funcao_ao_cliente_estar_pronto()


class ServicoPyro(ServicoDeRede):
    def __init__(
        self,
        info_de_conexao: InformacaoDeConexao,
        eh_anfitriao: bool,
        controlador_local: Any,
    ):
        super().__init__(
            info_de_conexao, eh_anfitriao, controlador_local=controlador_local
        )
        self.daemon_do_pyro = Pyro5.api.Daemon()
        self.controlador_local_para_expor_na_rede = ControladorPyro(
            self.controlador_local, self.eh_anfitriao, self._buscar_controlador_oponente
        )
        self.controlador_oponente = None

    def iniciar(self):
        servidor_de_nomes = Pyro5.api.locate_ns()
        uri = self.daemon_do_pyro.register(self.controlador_local_para_expor_na_rede)
        papel = "anfitriao" if self.eh_anfitriao else "oponente"
        servidor_de_nomes.register(f"{self.info_de_conexao.nome_da_sala}.{papel}", uri)
        print("URI:", uri)

        if not self.eh_anfitriao:
            self.controlador_oponente = Pyro5.api.Proxy(
                f"PYRONAME:{self.info_de_conexao.nome_da_sala}.anfitriao"
            )
            self.controlador_oponente.avisar_servidor_que_cliente_esta_pronto()
            self.controlador_oponente.atualizar_para_tela_de_jogo()

        thread_escutando_mensagens_dos_seletores: Thread = Thread(
            target=self._loop_escutando_pyro,
            daemon=True,
        )
        thread_escutando_mensagens_dos_seletores.start()

    def encerrar(self):
        pass

    def garantir_funcionamento_do_servico_de_rede(self):
        self.controlador_oponente._pyroClaimOwnership()

    def _loop_escutando_pyro(self):
        try:
            self.daemon_do_pyro.requestLoop()
        except KeyboardInterrupt:
            self.encerrar()

    def _obter_proxy_do_oponente(self):
        return

    def _buscar_controlador_oponente(self):
        self.controlador_oponente = Pyro5.api.Proxy(
            f"PYRONAME:{self.info_de_conexao.nome_da_sala}.oponente"
        )
