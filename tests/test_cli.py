from argparse import Namespace
from unittest import mock
from unittest.mock import MagicMock

import pytest

from gekitai.cli.erros import ModoNaoImplementado
from gekitai.cli.main import executa_modo, main


def test_erro_ao_tentar_executar_modo_inexistente():
    with pytest.raises(ModoNaoImplementado):
        executa_modo(argumentos=Namespace(modo="foo"))


def test_executa_modo_teste_inicial_corretamente():
    with mock.patch("gekitai.cli.main.executa_modo") as modo_executado:
        codigo_de_status_de_erro = main(["poc_grafico"])

    assert codigo_de_status_de_erro == 0
    modo_executado.assert_called_once_with(argumentos=Namespace(modo="poc_grafico"))
