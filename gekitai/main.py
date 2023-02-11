import argparse
import sys
from typing import Sequence

from gekitai import __version__


class Erro(Exception):
    def __init__(self, mensagem: str, codigo_de_status: int):
        self.mensagem = mensagem
        self.codigo_de_status = codigo_de_status

    def __str__(self):
        return self.mensagem


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

    parser_principal.add_argument("modo")

    argumentos_formatados = parser_principal.parse_args(argumentos)

    try:
        print(f"modo escolhido: {argumentos_formatados.modo}")
    except Erro as erro:
        print(erro.mensagem)
        return erro.codigo_de_status
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
