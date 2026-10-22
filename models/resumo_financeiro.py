class ResumoFinanceiro:
    def __init__(self):
        self.total_receitas = 0
        self.total_despesas = 0
        self.saldo_atual = 0

    def calcular_resumo(self, saldo_inicial, movimentacoes):
        self.total_receitas = 0
        self.total_despesas = 0
        
        for mov in movimentacoes:
            efeito = mov.efeito_no_saldo()
            if efeito > 0:
                self.total_receitas += efeito
            else:
                self.total_despesas += -efeito
        self.saldo_atual = saldo_inicial + self.total_receitas - self.total_despesas

    def mostrar_resumo(self):
        print(f"Total de Receitas: {self.total_receitas}")
        print(f"Total de Despesas: {self.total_despesas}")
        print(f"Saldo Atual: {self.saldo_atual}")