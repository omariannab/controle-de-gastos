class ContaFinanceira:
    def __init__(self):
        self.saldo_inicial = 0
        self.movimentacoes = []
        self.categorias = []

    def definir_saldo_inicial(self, valor):
        self.saldo_inicial = valor

    def adicionar_movimentacao(self, movimentacao):
        self.movimentacoes.append(movimentacao)

    def adicionar_categoria(self, categoria):
        self.categorias.append(categoria)

    def listar_movimentacoes(self):
        for i, movimentacao in enumerate(self.movimentacoes):
            print(f"{i + 1}.", end=" ")
            movimentacao.mostrar_dados()

    def excluir_movimentacao(self, indice):
        self.movimentacoes.pop(indice-1)

    def editar_movimentacao(self, indice, nova_descricao, novo_valor, nova_data, nova_categoria):
        self.movimentacoes[indice-1].editar_dados(nova_descricao, novo_valor, nova_data, nova_categoria)

    def calcular_saldo(self):
        saldo = self.saldo_inicial
        for movimentacao in self.movimentacoes:
            saldo += movimentacao.efeito_no_saldo()
        return saldo