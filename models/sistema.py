from models.usuario import Usuario

class SistemaControleGastos:
    def __init__(self):
        self.usuarios = []
        self.usuario_logado = None

    def cadastrar_usuario(self, nome, username, senha):
        for user in self.usuarios:
            if user.username == username:
                print("Erro: Nome de usuário já existe.")
                return False
        novo_usuario = Usuario(nome, username, senha)
        print(f"Usuário {nome} cadastrado com sucesso!")
        self.usuarios.append(novo_usuario)
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