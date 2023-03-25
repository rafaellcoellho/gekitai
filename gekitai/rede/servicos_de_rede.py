from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class InformacaoDeConexao(ABC):
    endereco: str
    porta: int


class ControladorDeOponente(ABC):
    @abstractmethod
    def informar_desistencia(self):
        pass

    @abstractmethod
    def passar_turno(self):
        pass

    @abstractmethod
    def adicionar_mensagem_no_chat(self, mensagem: str):
        pass

    @abstractmethod
    def criar_peca_no_tabuleiro(self, peca: int, linha: int, coluna: int):
        pass

    @abstractmethod
    def remover_peca_do_tabuleiro(
        self, linha: int, coluna: int, posicao_x_mouse: int, posicao_y_mouse: int
    ):
        pass


class ServicoDeRede(ABC):
    def __init__(
        self,
        info_de_conexao: InformacaoDeConexao,
        eh_anfitriao: bool,
        controlador_local: Any,
    ):
        self.info_de_conexao: InformacaoDeConexao = info_de_conexao
        self.eh_anfitriao: bool = eh_anfitriao
        self.controlador_local = controlador_local
        self.controlador_oponente: Optional[ControladorDeOponente] = None

    @abstractmethod
    def iniciar(self):
        pass

    @abstractmethod
    def encerrar(self):
        pass
