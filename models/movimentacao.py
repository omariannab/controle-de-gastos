class Movimentacao:
    def __init__(self, descricao, valor, data, categoria, id=None):
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria
        self.id = id

    def mostrar_dados(self):
        print(f"Descrição: {self.descricao}, Valor: {self.valor}, Data: {self.data}, Categoria: {self.categoria.nome}")

    def editar_dados(self, nova_descricao, novo_valor, nova_data, nova_categoria):
        self.descricao = nova_descricao
        self.valor = novo_valor
        self.data = nova_data
        self.categoria = nova_categoria

class Receita(Movimentacao):
    def efeito_no_saldo(self):
        return self.valor  

class Despesa(Movimentacao):
    def efeito_no_saldo(self):
        return -self.valor