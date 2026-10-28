class Categoria:
    def __init__(self, nome, descricao, id=None):
        self.nome = nome
        self.descricao = descricao
        self.id = id

    def mostrar_dados(self):
        print(f"Categoria: {self.nome}, Descrição: {self.descricao}")

    def alterar_nome(self, novo_nome):
        self.nome = novo_nome

    def alterar_descricao(self, nova_descricao):
        self.descricao = nova_descricao