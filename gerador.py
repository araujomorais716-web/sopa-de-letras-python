import random
import string

# Direções possíveis (variação de linha, variação de coluna)
DIRECOES = [
    (0, 1),    # →
    (0, -1),   # ←
    (1, 0),    # ↓
    (-1, 0),   # ↑
    (1, 1),    # ↘
    (-1, -1),  # ↖
    (1, -1),   # ↙
    (-1, 1),   # ↗
]


class GeradorSopa:

    def __init__(self, tamanho, palavras):
        self.tamanho = tamanho

        # Só palavras que cabem no tabuleiro; as maiores primeiro (mais fácil de encaixar)
        self.palavras = sorted(
            {p for p in palavras if 0 < len(p) <= tamanho},
            key=lambda p: (-len(p), p)
        )

        self.matriz = []
        self.posicoes = {}

    def _limpar(self):
        self.matriz = [[" " for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.posicoes = {}

    def gerar(self, max_tentativas=50):
        """Gera o tabuleiro. Se alguma palavra não couber, recomeça do zero."""
        for _ in range(max_tentativas):
            self._limpar()

            if all(self.colocar_palavra(p) for p in self.palavras):
                break

        self.preencher()
        return self.matriz

    def colocar_palavra(self, palavra):
        """Tenta colocar a palavra. Devolve True se conseguiu."""
        for _ in range(500):
            direcao = random.choice(DIRECOES)
            linha = random.randint(0, self.tamanho - 1)
            coluna = random.randint(0, self.tamanho - 1)

            if self.pode_colocar(palavra, linha, coluna, direcao):
                self.escrever_palavra(palavra, linha, coluna, direcao)
                return True

        return False

    def pode_colocar(self, palavra, linha, coluna, direcao):
        d_linha, d_coluna = direcao

        # Verifica logo se a palavra cabe de ponta a ponta
        fim_linha = linha + d_linha * (len(palavra) - 1)
        fim_coluna = coluna + d_coluna * (len(palavra) - 1)

        if not (0 <= fim_linha < self.tamanho and 0 <= fim_coluna < self.tamanho):
            return False

        for letra in palavra:
            atual = self.matriz[linha][coluna]

            if atual != " " and atual != letra:
                return False

            linha += d_linha
            coluna += d_coluna

        return True

    def escrever_palavra(self, palavra, linha, coluna, direcao):
        d_linha, d_coluna = direcao
        posicoes = []

        for letra in palavra:
            self.matriz[linha][coluna] = letra
            posicoes.append((linha, coluna))

            linha += d_linha
            coluna += d_coluna

        self.posicoes[palavra] = posicoes

    def preencher(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.matriz[i][j] == " ":
                    self.matriz[i][j] = random.choice(string.ascii_uppercase)

    def obter_posicoes(self):
        return self.posicoes

    def obter_palavras(self):
        """Só as palavras que realmente estão no tabuleiro, por ordem alfabética."""
        return sorted(self.posicoes.keys())