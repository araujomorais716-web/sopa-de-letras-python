import os
import unicodedata

# Caminho absoluto: funciona mesmo que o jogo seja iniciado de outra pasta
PASTA_TEMAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temas")


def _normalizar(texto):
    """Põe em maiúsculas, remove acentos e mantém só letras A-Z."""
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acentos = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return "".join(c for c in sem_acentos.upper() if c.isascii() and c.isalpha())


def listar_temas():
    """Devolve os nomes dos temas existentes na pasta 'temas'."""
    if not os.path.isdir(PASTA_TEMAS):
        return []

    temas = [
        os.path.splitext(nome)[0]
        for nome in os.listdir(PASTA_TEMAS)
        if nome.lower().endswith(".txt")
    ]
    return sorted(temas, key=str.lower)


def carregar_palavras(nome_tema):
    """Carrega as palavras do tema (sem repetidas, sem acentos, em maiúsculas)."""
    caminho = os.path.join(PASTA_TEMAS, f"{nome_tema}.txt")

    if not os.path.exists(caminho):
        return []

    palavras = []

    with open(caminho, "r", encoding="utf-8") as ficheiro:
        for linha in ficheiro:
            palavra = _normalizar(linha)

            if palavra and palavra not in palavras:
                palavras.append(palavra)

    return palavras