from dataclasses import dataclass


class Erro(Exception):
    def __init__(self, mensagem: str, codigo_de_status: int):
        self.mensagem: str = mensagem
        self.codigo_de_status: int = codigo_de_status

    def __str__(self) -> str:
        return self.mensagem


@dataclass
class ModoNaoImplementado(Erro):
    mensagem: str = "Modo inválido"
    codigo_de_status: int = 1
