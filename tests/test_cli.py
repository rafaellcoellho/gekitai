from unittest.mock import MagicMock

import pytest

from gekitai.main import ModoNaoImplementado, executa_modo


def test_erro_ao_tentar_executar_modo_inexistente(capsys):
    with pytest.raises(ModoNaoImplementado):
        argumentos = MagicMock()
        argumentos.modo = "foo"
        executa_modo(argumentos=argumentos)
