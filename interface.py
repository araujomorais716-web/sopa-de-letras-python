import tkinter as tk
from tkinter import messagebox

from configuracoes import (
    TAMANHO_TABULEIRO, ERROS_MAXIMOS, TEMA_PADRAO, TITULO,
    LARGURA_JANELA, ALTURA_JANELA,
    COR_FUNDO, COR_BOTAO, COR_CELULA, COR_SELECAO, COR_ACERTO,
    COR_ERRO, COR_PONTOS, FONTE_TITULO,
)
from palavras import carregar_palavras, listar_temas
from gerador import GeradorSopa


class Interface:

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title(TITULO)
        self.janela.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")
        self.janela.configure(bg=COR_FUNDO)

        # Os temas são lidos da pasta "temas" (basta adicionar um .txt para criar um novo)
        self.temas = listar_temas()

        if not self.temas:
            messagebox.showerror(
                "Erro",
                "Nenhum tema encontrado.\nCrie ficheiros .txt dentro da pasta 'temas'."
            )
            self.janela.destroy()
            raise SystemExit(1)

        self.tema_atual = TEMA_PADRAO if TEMA_PADRAO in self.temas else self.temas[0]

        # Widgets dinâmicos
        self.botoes = []
        self.lista_labels = {}

        self.preparar_jogo()
        self.criar_interface()

    # ------------------------------------------------------------------
    # LÓGICA DO JOGO
    # ------------------------------------------------------------------
    def preparar_jogo(self):
        """Gera um novo tabuleiro e repõe o estado do jogo."""
        palavras = carregar_palavras(self.tema_atual)

        self.gerador = GeradorSopa(TAMANHO_TABULEIRO, palavras)
        self.matriz = self.gerador.gerar()
        self.posicoes = self.gerador.obter_posicoes()
        self.palavras = self.gerador.obter_palavras()

        self.selecao = []
        self.palavras_encontradas = set()
        self.celulas_encontradas = set()

        self.erros = 0
        self.pontos = 0

    def cor_base(self, linha, coluna):
        """Cor normal de uma célula (verde se já faz parte de uma palavra encontrada)."""
        if (linha, coluna) in self.celulas_encontradas:
            return COR_ACERTO
        return COR_CELULA

    # ------------------------------------------------------------------
    # INTERFACE
    # ------------------------------------------------------------------
    def criar_interface(self):
        tk.Label(
            self.janela,
            text="SOPA DE LETRAS",
            font=FONTE_TITULO,
            bg=COR_FUNDO
        ).pack(pady=10)

        # Barra superior
        barra = tk.Frame(self.janela, bg=COR_FUNDO)
        barra.pack(pady=5)

        tk.Label(
            barra,
            text="Tema:",
            bg=COR_FUNDO,
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=5)

        self.tema_var = tk.StringVar(value=self.tema_atual)

        opcoes = tk.OptionMenu(
            barra,
            self.tema_var,
            *self.temas,
            command=self.mudar_tema
        )
        opcoes.pack(side="left", padx=10)

        tk.Button(
            barra,
            text="Novo Jogo",
            bg=COR_BOTAO,
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.novo_jogo
        ).pack(side="left", padx=10)

        # Área principal
        principal = tk.Frame(self.janela, bg=COR_FUNDO)
        principal.pack()

        self.frame_tabuleiro = tk.Frame(principal, bg=COR_FUNDO)
        self.frame_tabuleiro.grid(row=0, column=0, padx=20)

        self.lateral = tk.Frame(principal, bg=COR_FUNDO)
        self.lateral.grid(row=0, column=1, padx=30, sticky="n")

        tk.Label(
            self.lateral,
            text="PALAVRAS",
            font=("Arial", 16, "bold"),
            bg=COR_FUNDO
        ).pack(pady=5)

        self.frame_lista_palavras = tk.Frame(self.lateral, bg=COR_FUNDO)
        self.frame_lista_palavras.pack()

        self.lbl_erros = tk.Label(
            self.lateral,
            font=("Arial", 13, "bold"),
            bg=COR_FUNDO,
            fg=COR_ERRO
        )
        self.lbl_erros.pack(pady=15)

        self.lbl_pontos = tk.Label(
            self.lateral,
            font=("Arial", 13, "bold"),
            bg=COR_FUNDO,
            fg=COR_PONTOS
        )
        self.lbl_pontos.pack()

        self.atualizar_placar()
        self.desenhar_elementos_dinamicos()

    def atualizar_placar(self):
        self.lbl_erros.config(text=f"Erros: {self.erros}/{ERROS_MAXIMOS}")
        self.lbl_pontos.config(text=f"Pontos: {self.pontos}")

    def desenhar_elementos_dinamicos(self):
        """Cria os botões do tabuleiro e a lista de palavras do jogo atual."""
        for linha in self.botoes:
            for botao in linha:
                botao.destroy()
        self.botoes.clear()

        for i in range(TAMANHO_TABULEIRO):
            linha = []
            for j in range(TAMANHO_TABULEIRO):
                botao = tk.Button(
                    self.frame_tabuleiro,
                    text=self.matriz[i][j],
                    width=2,
                    height=1,
                    font=("Arial", 11, "bold"),
                    bg=COR_CELULA,
                    command=lambda l=i, c=j: self.clicar_letra(l, c)
                )
                botao.grid(row=i, column=j)
                linha.append(botao)
            self.botoes.append(linha)

        for lbl in self.lista_labels.values():
            lbl.destroy()
        self.lista_labels.clear()

        for palavra in self.palavras:
            lbl = tk.Label(
                self.frame_lista_palavras,
                text=palavra,
                font=("Arial", 13),
                bg=COR_FUNDO,
                fg="black"
            )
            lbl.pack(anchor="w")
            self.lista_labels[palavra] = lbl

    # ------------------------------------------------------------------
    # EVENTOS
    # ------------------------------------------------------------------
    def mudar_tema(self, novo_tema):
        self.tema_atual = novo_tema
        self.novo_jogo()

    def clicar_letra(self, linha, coluna):
        """Regista os cliques do jogador (clicar de novo na mesma letra desmarca-a)."""
        if (linha, coluna) in self.selecao:
            self.selecao.remove((linha, coluna))
            self.botoes[linha][coluna].configure(bg=self.cor_base(linha, coluna))
            return

        self.selecao.append((linha, coluna))
        self.botoes[linha][coluna].configure(bg=COR_SELECAO)

        if len(self.selecao) == 2:
            self.verificar_palavra()

    def verificar_palavra(self):
        inicio, fim = self.selecao
        self.selecao = []

        for palavra, posicoes in self.posicoes.items():
            if palavra in self.palavras_encontradas:
                continue

            if (posicoes[0], posicoes[-1]) in ((inicio, fim), (fim, inicio)):
                self.palavra_encontrada(palavra, posicoes)
                return

        self.palavra_errada(inicio, fim)

    def palavra_encontrada(self, palavra, posicoes):
        self.palavras_encontradas.add(palavra)
        self.pontos += 10
        self.atualizar_placar()

        for l, c in posicoes:
            self.celulas_encontradas.add((l, c))
            self.botoes[l][c].configure(bg=COR_ACERTO, fg="black")

        self.lista_labels[palavra].config(fg="green", font=("Arial", 13, "bold"))

        if len(self.palavras_encontradas) == len(self.posicoes):
            messagebox.showinfo("Parabéns!", "Você encontrou todas as palavras!")
            self.novo_jogo()

    def palavra_errada(self, inicio, fim):
        self.erros += 1
        self.atualizar_placar()

        # Repõe a cor correta (sem apagar o verde das palavras já encontradas)
        for l, c in (inicio, fim):
            self.botoes[l][c].configure(bg=self.cor_base(l, c))

        messagebox.showwarning("Erro", "Palavra incorreta!")

        if self.erros >= ERROS_MAXIMOS:
            messagebox.showinfo("Fim do jogo", "Você perdeu!")
            self.novo_jogo()

    def novo_jogo(self):
        """Reinicia o jogo mantendo a janela aberta."""
        self.preparar_jogo()
        self.atualizar_placar()
        self.desenhar_elementos_dinamicos()

    def executar(self):
        self.janela.mainloop()


if __name__ == "__main__":
    Interface().executar()