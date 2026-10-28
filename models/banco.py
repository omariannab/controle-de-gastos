import sqlite3

class BancoDeDados:
    def __init__(self):
        self.conexao = sqlite3.connect("controle_gastos.db")
        self.cursor = self.conexao.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    username TEXT UNIQUE,
                    senha TEXT,
                    saldo_inicial REAL
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    descricao TEXT,
                    usuario_id INTEGER
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS movimentacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT,
                    descricao TEXT,
                    valor REAL,
                    data TEXT,
                    categoria_id INTEGER,
                    usuario_id INTEGER
                )
            """)

            self.conexao.commit()

    def salvar_usuario(self, nome, username, senha):
        self.cursor.execute(
            "INSERT INTO usuarios (nome, username, senha, saldo_inicial) VALUES (?, ?, ?, ?)",  
            (nome, username, senha, 0)                                               
        )

        self.conexao.commit()
        return self.cursor.lastrowid

    def buscar_usuarios(self):
        self.cursor.execute("SELECT id, nome, username, senha, saldo_inicial FROM usuarios")
        return self.cursor.fetchall()

    def atualizar_saldo_inicial(self, id_usuario, valor):
        self.cursor.execute("UPDATE usuarios SET saldo_inicial = ? WHERE id = ?", (valor, id_usuario))
        self.conexao.commit()

    def salvar_categoria(self, nome, descricao, usuario_id):
         self.cursor.execute("INSERT INTO categorias (nome, descricao, usuario_id) VALUES (?, ?, ?)", (nome, descricao, usuario_id))
         self.conexao.commit()
         return self.cursor.lastrowid

    def atualizar_categoria(self, novo_nome, nova_descricao, id_categoria):
         self.cursor.execute("UPDATE categorias SET nome = ?, descricao = ? WHERE id = ?", (novo_nome, nova_descricao, id_categoria))
         self.conexao.commit()

    def buscar_categorias(self, usuario_id):
         self.cursor.execute("SELECT id, nome, descricao FROM categorias WHERE usuario_id = ?", (usuario_id,))
         return self.cursor.fetchall()

    def salvar_movimentacao(self, tipo, descricao, valor, data, categoria_id, usuario_id):
        self.cursor.execute("""
            INSERT INTO movimentacoes (tipo, descricao, valor, data, categoria_id, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tipo, descricao, valor, data, categoria_id, usuario_id))
        self.conexao.commit()
        return self.cursor.lastrowid

    def excluir_movimentacao(self, id_movimentacao):
         self.cursor.execute("DELETE FROM movimentacoes WHERE id = ?", (id_movimentacao,))
         self.conexao.commit()

    def atualizar_movimentacao(self, nova_descricao, novo_valor, nova_data, id_categoria, id_movimentacao):
        self.cursor.execute("""
            UPDATE movimentacoes
            SET descricao = ?, valor = ?, data = ?, categoria_id = ?
            WHERE id = ?
        """, (nova_descricao, novo_valor, nova_data, id_categoria, id_movimentacao))
        self.conexao.commit()

    def buscar_movimentacoes(self, usuario_id):
            self.cursor.execute("""
            SELECT id, tipo, descricao, valor, data, categoria_id
            FROM movimentacoes 
            WHERE usuario_id = ?
            """, (usuario_id,))
            return self.cursor.fetchall()