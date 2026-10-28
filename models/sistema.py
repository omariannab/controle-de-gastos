from models.usuario import Usuario
from models.banco import BancoDeDados
from models.categoria import Categoria
from models.movimentacao import Receita, Despesa

class SistemaControleGastos:
    def __init__(self):
        self.usuarios = []
        self.usuario_logado = None
        self.banco = BancoDeDados()
        for linha_users in self.banco.buscar_usuarios():
            usuario = Usuario(linha_users[1], linha_users[2], linha_users[3], linha_users[0])
            self.usuarios.append(usuario)
            usuario.conta_financeira.definir_saldo_inicial(linha_users[4])
            for linha_cat in self.banco.buscar_categorias(usuario.id):
                categoria = Categoria(linha_cat[1], linha_cat[2], linha_cat[0])
                usuario.conta_financeira.adicionar_categoria(categoria)
            for linha_mov in self.banco.buscar_movimentacoes(usuario.id):
                for cat in usuario.conta_financeira.categorias:   
                    if cat.id == linha_mov[5]:                   
                        categoria_mov = cat                       
                if linha_mov[1] == "receita":
                    receita = Receita(linha_mov[2], linha_mov[3], linha_mov[4], categoria_mov, linha_mov[0])
                    usuario.conta_financeira.adicionar_movimentacao(receita)
                else: 
                    despesa = Despesa(linha_mov[2], linha_mov[3], linha_mov[4], categoria_mov, linha_mov[0])
                    usuario.conta_financeira.adicionar_movimentacao(despesa)

    def cadastrar_usuario(self, nome, username, senha):
        for user in self.usuarios:
            if user.username == username:
                print("Erro: Nome de usuário já existe.")
                return False
        novo_usuario = Usuario(nome, username, senha)
        print(f"Usuário {nome} cadastrado com sucesso!")
        self.usuarios.append(novo_usuario)
        novo_usuario.id = self.banco.salvar_usuario(nome, username, senha)
        return True

    def realizar_login(self, username, senha):
        for user in self.usuarios:
            if user.username == username and user.verificar_senha(senha):
                self.usuario_logado = user
                print(f"Login bem-sucedido! Bem-vindo, {user.nome}.")
                return True
        print("Login falhou. Verifique seu nome de usuário e senha.")
        return False

    def encerrar_sessao(self):
        self.usuario_logado = None