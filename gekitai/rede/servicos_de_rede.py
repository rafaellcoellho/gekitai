from abc import abstractmethod, ABC
from dataclasses import dataclass
from collections.abc import Callable


class FuncaoExecutadaAoReceberMensagem(ABC):
    @abstractmethod
    def __call__(self, mensagem: str) -> None:
        pass


@dataclass
class InformacaoDeConexao(ABC):
    endereco: str
    porta: int


class ServicoDeRede(ABC):
    def __init__(self, info_de_conexao: InformacaoDeConexao, eh_anfitriao: bool):
        self.info_de_conexao: InformacaoDeConexao = info_de_conexao
        self.eh_anfitriao: bool = eh_anfitriao

    @abstractmethod
    def iniciar(self, ao_receber_mensagens: FuncaoExecutadaAoReceberMensagem):
        pass

    @abstractmethod
    def enviar_mensagem(self, mensagem: str):
        pass

    @abstractmethod
    def encerrar(self):
        pass
