import argparse
import sys
from typing import Sequence

from gekitai import __version__
from gekitai.cli.erros import Erro, ModoNaoImplementado
from gekitai.pocs.chat import modo_exemplo_chat
from gekitai.pocs.grafico import modo_exemplo_grafico


def executa_modo(argumentos: argparse.Namespace):
    if argumentos.modo == "poc_grafico":
        modo_exemplo_grafico()
    elif argumentos.modo == "poc_chat":
        modo_exemplo_chat()
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

    subparsers.add_parser("poc_grafico", help="mostrar poc de gráfico usando pygame")
    subparsers.add_parser(
        "poc_chat",
        help="mostrar poc de um chat peer to peer usando pygame, pygame_gui e sockets",
    )

    if len(argumentos) == 0:
        argumentos = ["poc_grafico"]
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
