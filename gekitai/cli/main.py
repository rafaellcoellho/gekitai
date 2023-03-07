import argparse
import sys
from typing import Sequence

from gekitai import __version__
from gekitai.cli.erros import Erro, ModoNaoImplementado
from gekitai.jogo.main import main as modo_jogo
from gekitai.pocs.chat import modo_exemplo_chat_servidor, modo_exemplo_chat_cliente
from gekitai.pocs.grafico import modo_exemplo_grafico
from gekitai.pocs.interface_jogo import modo_exemplo_interface_de_jogo


def executa_modo(argumentos: argparse.Namespace):
    if argumentos.modo == "poc_grafico":
        modo_exemplo_grafico()
    elif argumentos.modo == "poc_chat":
        if argumentos.papel == "servidor":
            modo_exemplo_chat_servidor(porta=argumentos.porta)
        else:
            modo_exemplo_chat_cliente(ip=argumentos.ip, porta=argumentos.porta)
    elif argumentos.modo == "poc_jogo":
        modo_exemplo_interface_de_jogo()
    elif argumentos.modo == "jogo":
        modo_jogo(
            papel=argumentos.papel,
            ip=argumentos.ip if argumentos.papel == "cliente" else "127.0.0.1",
            porta=argumentos.porta,
        )
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

    # prova de conceito dos gráficos
    subparsers.add_parser("poc_grafico", help="mostrar poc de gráfico usando pygame")

    # prova de conceito do chat
    parser_modo_poc_chat = subparsers.add_parser(
        "poc_chat",
        help="mostrar poc de um chat peer to peer usando pygame, pygame_gui e sockets",
    )
    subparsers_poc_chat = parser_modo_poc_chat.add_subparsers(dest="papel")

    parser_servidor_poc_chat = subparsers_poc_chat.add_parser(
        "servidor", help="instância chat com papal de servidor"
    )
    parser_servidor_poc_chat.add_argument(
        "porta", help="porta em que o servidor vai escutar clientes se conectando"
    )

    parser_cliente_poc_chat = subparsers_poc_chat.add_parser(
        "cliente", help="instância chat com papal de cliente"
    )
    parser_cliente_poc_chat.add_argument("ip", help="endereço ip do servidor")
    parser_cliente_poc_chat.add_argument(
        "porta", help="porta em que o servidor vai estar escutando"
    )

    # prova de conceito da interface de jogo
    subparsers.add_parser("poc_jogo", help="mostrar poc da interface de jogo")

    # interface do jogo (ainda sem menu)
    parser_modo_jogo = subparsers.add_parser("jogo", help="executa o jogo")
    subparsers_poc_chat = parser_modo_jogo.add_subparsers(dest="papel")

    parser_servidor_jogo = subparsers_poc_chat.add_parser(
        "servidor", help="instância jogo servidor"
    )
    parser_servidor_jogo.add_argument(
        "porta", help="servidor usará essa porta para escutar cliente"
    )

    parser_cliente_jogo = subparsers_poc_chat.add_parser(
        "cliente", help="instância jogo cliente"
    )
    parser_cliente_jogo.add_argument("ip", help="endereço ip do jogo servidor")
    parser_cliente_jogo.add_argument(
        "porta", help="conecta nessa porta para iniciar comunicação com servidor"
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
