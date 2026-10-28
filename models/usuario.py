from models.conta_financeira import ContaFinanceira

class Usuario:
    def __init__(self, nome, username, senha, id=None):
        self.nome = nome
        self.username = username
        self.senha = senha
        self.conta_financeira = ContaFinanceira()   
        self.id = id  

    def mostrar_dados(self):
        print(f"Nome: {self.nome}, Username: {self.username}")

    def verificar_senha(self, senha_digitada):
            return self.senha == senha_digitada
