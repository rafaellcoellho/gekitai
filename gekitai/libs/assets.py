import sys
from pathlib import Path


def obter_caminho_para_pasta_de_assets(nome_do_arquivo: str, caminho_para_arquivo: str):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(caminho_para_arquivo).resolve().with_name(nome_do_arquivo)
    else:
        return f"assets/{nome_do_arquivo}"
