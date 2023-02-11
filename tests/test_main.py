from gekitai.main import main


def test_inicial(capsys):
    main(["foo"])
    result = capsys.readouterr()
    assert result.out == "modo escolhido: foo\n"
