import argparse
import sys
from dataclasses import dataclass
from typing import Sequence

from gekitai import __version__
from gekitai.pocs.logo_quicando import executar_logo_quicando


class Erro(Exception):
    def __init__(self, mensagem: str, codigo_de_status: int):
        self.mensagem = mensagem
        self.codigo_de_status = codigo_de_status

    def __str__(self):
        return self.mensagem


@dataclass
class ModoNaoImplementado(Erro):
    mensagem: str = "Modo inválido"
    codigo_de_status: int = 1


def executa_modo(argumentos: argparse.Namespace):
    if argumentos.modo == "teste":
        executar_logo_quicando()
    else:
        raise ModoNaoImplementado


def main(argv: Sequence[str] | None = None):
    argumentos = argv if argv is not None else sys.argv[1:]
    parser_principal = argparse.ArgumentParser(
        prog="gekitai",
        description="Programa para a disciplina de PPD do curso de eng. da computação no IFCE do semestre 2023.1",
        epilog="Autor: Rafael Coelho (rafaellcoellho@gmail.com)",
        add_help=False,
    )

    versao = f"{__version__}"
    parser_principal.add_argument(
        "-v",
        "--version",
        action="version",
        version=versao,
        help="mostra versão do aplicativo",
    )
    parser_principal.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="mostra ajuda do programa",
    )

    subparsers = parser_principal.add_subparsers(dest="modo")

    subparsers.add_parser("logo", help="mostrar logo do gekitai quicando pela tela")

    if len(argumentos) == 0:
        argumentos = ["teste"]
    argumentos_formatados = parser_principal.parse_args(argumentos)

    try:
        executa_modo(argumentos=argumentos_formatados)
    except Erro as erro:
        print(erro.mensagem)
        return erro.codigo_de_status
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
