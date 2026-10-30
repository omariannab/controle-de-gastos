import ttkbootstrap as ttk
from models.sistema import SistemaControleGastos
from ttkbootstrap.dialogs import Messagebox
from models.categoria import Categoria
from models.movimentacao import Receita, Despesa
from models.resumo_financeiro import ResumoFinanceiro

sistema = SistemaControleGastos()

janela = ttk.Window(title="Controle de Gastos", themename="flatly")
janela.geometry("800x640")
janela.minsize(800, 640)
janela.attributes("-zoomed", True)

estilo = janela.style
estilo.configure("TNotebook.Tab", font=("Ubuntu", 12), padding=(20, 10))
estilo.configure("Treeview", font=("Ubuntu", 12), rowheight=60)
estilo.configure("Treeview.Heading", font=("Ubuntu", 12, "bold"))
estilo.map("Treeview",
           background=[("selected", "#dbe7f5")],
           foreground=[("selected", "#1f2d3d")])
estilo.configure("TButton", font=("Ubuntu", 12))
estilo.configure("TLabel", font=("Ubuntu", 12))
cor_fundo = "#f4f6f9"
estilo.configure("Link.TButton", background=cor_fundo)
estilo.configure("success.TLabel", background=cor_fundo)
estilo.map("Link.TButton", background=[("active", cor_fundo)])
estilo.configure("danger.TLabel", background=cor_fundo)
estilo.configure("TFrame", background=cor_fundo)
estilo.configure("TLabel", background=cor_fundo)
estilo.configure("TNotebook", background=cor_fundo)
janela.configure(background=cor_fundo)

def limpar_tela():
    for widget in janela.winfo_children():
        widget.destroy()

area_inicial = None

def preparar_tela_inicial():
    global area_inicial

    if area_inicial is not None and area_inicial.winfo_exists():
        for widget in area_inicial.winfo_children():
            widget.destroy()
    else:
        limpar_tela()

        painel = ttk.Frame(janela, bootstyle="primary", width=1000)
        painel.pack(side="left", fill="y")
        painel.pack_propagate(False)

        nome_app = ttk.Label(painel, text="Controle\nde Gastos", font=("Ubuntu", 36, "bold"),
                             bootstyle="inverse-primary", justify="center")
        nome_app.pack(expand=True)

        area_inicial = ttk.Frame(janela)
        area_inicial.pack(side="left", fill="both", expand=True)

    quadro = ttk.Frame(area_inicial, padding=50)
    quadro.pack(expand=True)
    return quadro

def mostrar_login(mensagem=""):
    quadro = preparar_tela_inicial()

    titulo = ttk.Label(quadro, text="Entrar", font=("Ubuntu", 26, "bold"))
    titulo.pack(anchor="w", pady=(0, 25))

    texto_usuario = ttk.Label(quadro, text="Usuário", font=("Ubuntu", 14))
    texto_usuario.pack(anchor="w")
    campo_usuario = ttk.Entry(quadro, font=("Ubuntu", 14), width=28)
    campo_usuario.pack(pady=(2, 15), ipady=4)

    texto_senha = ttk.Label(quadro, text="Senha", font=("Ubuntu", 14))
    texto_senha.pack(anchor="w")
    campo_senha = ttk.Entry(quadro, font=("Ubuntu", 14), width=28, show="*")
    campo_senha.pack(pady=(2, 25), ipady=4)

    texto_erro = ttk.Label(quadro, text="", bootstyle="danger", font=("Ubuntu", 11))
    texto_erro.pack(pady=(0, 10))

    if mensagem != "":
        texto_erro.config(text=mensagem, bootstyle="success")

    def entrar():
        usuario = campo_usuario.get()
        senha = campo_senha.get()
        if sistema.realizar_login(usuario, senha):
            mostrar_conta()
        else:
            texto_erro.config(text="Usuário ou senha incorretos.", bootstyle="danger")

    botao_entrar = ttk.Button(quadro, text="Entrar", command=entrar, bootstyle="primary")
    botao_entrar.pack(fill="x", ipady=5)

    botao_cadastrar = ttk.Button(quadro, text="Cadastre-se", command=mostrar_cadastro, bootstyle="link")
    botao_cadastrar.pack(pady=(10, 0))

def mostrar_cadastro():
    quadro = preparar_tela_inicial()

    titulo = ttk.Label(quadro, text="Cadastro", font=("Ubuntu", 26, "bold"))
    titulo.pack(anchor="w", pady=(0, 25))

    texto_nome = ttk.Label(quadro, text="Nome", font=("Ubuntu", 14))
    texto_nome.pack(anchor="w")
    campo_nome = ttk.Entry(quadro, font=("Ubuntu", 14), width=28)
    campo_nome.pack(pady=(2, 15), ipady=4)

    texto_usuario = ttk.Label(quadro, text="Usuário", font=("Ubuntu", 14))
    texto_usuario.pack(anchor="w")
    campo_usuario = ttk.Entry(quadro, font=("Ubuntu", 14), width=28)
    campo_usuario.pack(pady=(2, 15), ipady=4)

    texto_senha = ttk.Label(quadro, text="Senha", font=("Ubuntu", 14))
    texto_senha.pack(anchor="w")
    campo_senha = ttk.Entry(quadro, font=("Ubuntu", 14), width=28, show="*")
    campo_senha.pack(pady=(2, 25), ipady=4)

    texto_erro = ttk.Label(quadro, text="", bootstyle="danger", font=("Ubuntu", 11))
    texto_erro.pack(pady=(0, 10))

    def cadastrar():
            nome = campo_nome.get()
            usuario = campo_usuario.get()
            senha = campo_senha.get()
            if nome == "" or usuario == "" or senha == "":
                texto_erro.config(text="Preencha todos os campos.", bootstyle="danger")
            else:
                if sistema.cadastrar_usuario(nome, usuario, senha):
                    mostrar_login("Usuário cadastrado com sucesso!")
                else:
                    texto_erro.config(text="Esse nome de usuário já existe.")

    botao_cadastrar = ttk.Button(quadro, text="Cadastrar", command=cadastrar, bootstyle="primary")
    botao_cadastrar.pack(fill="x", ipady=5)

    botao_voltar = ttk.Button(quadro, text="Voltar", command=mostrar_login, bootstyle="link")
    botao_voltar.pack(pady=(10, 0))

def mostrar_conta():
    limpar_tela()

    topo = ttk.Frame(janela, padding=25, bootstyle="primary")
    topo.pack(fill="x")

    dados_usuario = ttk.Frame(topo, bootstyle="primary")
    dados_usuario.pack(side="left")

    saudacao = ttk.Label(dados_usuario, text=f"Olá, {sistema.usuario_logado.nome}", font=("Ubuntu", 18, "bold"), bootstyle="inverse-primary")
    saudacao.pack(anchor="w")

    username = ttk.Label(dados_usuario, text=f"@{sistema.usuario_logado.username}", font=("Ubuntu", 12), bootstyle="inverse-primary")
    username.pack(anchor="w")

    def sair():
            sistema.encerrar_sessao()
            mostrar_login()

    botao_sair = ttk.Button(topo, text="Sair", command=sair, bootstyle="light")
    botao_sair.pack(side="right")

    abas = ttk.Notebook(janela)
    abas.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    #------------- Movimentações --------------

    aba_movimentacoes = ttk.Frame(abas, padding=15)
    abas.add(aba_movimentacoes, text="Movimentações")

    tabela_mov = ttk.Treeview(aba_movimentacoes, columns=("descricao", "tipo", "valor", "data", "categoria"), show="headings")
    tabela_mov.heading("descricao", text="Descrição", anchor="w")
    tabela_mov.heading("tipo", text="Tipo", anchor="w")
    tabela_mov.heading("valor", text="Valor", anchor="w")
    tabela_mov.heading("data", text="Data", anchor="w")
    tabela_mov.heading("categoria", text="Categoria", anchor="w")
    tabela_mov.tag_configure("impar", background="#f2f4f7")
    tabela_mov.tag_configure("receita", foreground="#18a058")
    tabela_mov.tag_configure("despesa", foreground="#d03050")
    tabela_mov.pack(fill="both", expand=True)

    def atualizar_tabela_movimentacoes():
        tabela_mov.delete(*tabela_mov.get_children())
        for i, mov in enumerate(sistema.usuario_logado.conta_financeira.movimentacoes):
            cor = "par" if i % 2 == 0 else "impar"
            if mov.efeito_no_saldo() > 0:
                tipo = "Receita"
                valor = f"+ R$ {mov.valor:.2f}"
                tag_tipo = "receita"
            else:
                tipo = "Despesa"
                valor = f"- R$ {mov.valor:.2f}"
                tag_tipo = "despesa"
            tabela_mov.insert("", "end", values=(mov.descricao, tipo, valor, mov.data, mov.categoria.nome), tags=(cor, tag_tipo))

    atualizar_tabela_movimentacoes()

    barra_botoes_mov = ttk.Frame(aba_movimentacoes)
    barra_botoes_mov.pack(fill="x", pady=(15, 0))

    def nova_movimentacao(tipo):
        janelinha = ttk.Toplevel(title="Nova movimentação")
        janelinha.configure(background=cor_fundo)
        janelinha.resizable(False, False)
        janelinha.transient(janela)
        janelinha.grab_set()
    
        quadro = ttk.Frame(janelinha, padding=40)
        quadro.pack(expand=True)

        texto_descricao = ttk.Label(quadro, text="Descrição", font=("Ubuntu", 12))
        texto_descricao.pack(anchor="w")
        campo_descricao = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_descricao.pack(pady=(2, 15), ipady=4)

        texto_valor = ttk.Label(quadro, text="Valor", font=("Ubuntu", 12))
        texto_valor.pack(anchor="w")
        campo_valor = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_valor.pack(pady=(2, 15), ipady=4) 

        texto_data = ttk.Label(quadro, text="Data (DD-MM-AAAA)", font=("Ubuntu", 12))
        texto_data.pack(anchor="w")
        campo_data = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_data.pack(pady=(2, 15), ipady=4)

        texto_categoria = ttk.Label(quadro, text="Categoria", font=("Ubuntu", 12))
        texto_categoria.pack(anchor="w")
        categorias = []
        for cat in sistema.usuario_logado.conta_financeira.categorias:
            categorias.append(cat.nome)    
        campo_categoria = ttk.Combobox(quadro, values=categorias, state="readonly", font=("Ubuntu", 12), width=26)
        campo_categoria.pack(pady=(2, 25), ipady=4)

        texto_erro = ttk.Label(quadro, text="", bootstyle="danger", font=("Ubuntu", 11))
        texto_erro.pack(pady=(0, 10))
    
        def salvar():
            descricao = campo_descricao.get()
            valor = campo_valor.get()
            data = campo_data.get()
            posicao_categoria = campo_categoria.current()
            if descricao == "" or valor == "" or data == "" or posicao_categoria == -1:
                texto_erro.config(text="Preencha todos os campos.")
            else: 
                try:
                    valor = float(valor.replace(",", "."))
                except ValueError:
                    texto_erro.config(text="O valor precisa ser um número.")
                    return
                categoria = sistema.usuario_logado.conta_financeira.categorias[posicao_categoria]
                if tipo == "receita":
                    movimentacao = Receita(descricao, valor, data, categoria)
                else:
                    movimentacao = Despesa(descricao, valor, data, categoria)
                sistema.usuario_logado.conta_financeira.adicionar_movimentacao(movimentacao)
                movimentacao.id = sistema.banco.salvar_movimentacao(tipo, descricao, valor, data, categoria.id, sistema.usuario_logado.id)
                atualizar_tabela_movimentacoes()
                janelinha.destroy()
                        
        botao_salvar = ttk.Button(quadro, text="Salvar", command=salvar, bootstyle="primary")
        botao_salvar.pack(fill="x", ipady=5)

    botao_adcreceita = ttk.Button(barra_botoes_mov, text="+ Receita", command=lambda: nova_movimentacao("receita"), bootstyle="success")
    botao_adcreceita.pack(side="left", ipady=5, ipadx=15)

    botao_adcdespesa = ttk.Button(barra_botoes_mov, text="+ Despesa", command=lambda: nova_movimentacao("despesa"), bootstyle="danger")
    botao_adcdespesa.pack(side="left", padx=(10, 0),ipady=5, ipadx=15)

    def editar_mov():
        selecionadas = tabela_mov.selection()
        
        if len(selecionadas) == 0:
            Messagebox.show_warning("Selecione uma movimentação na tabela.", "Atenção")
            return
    
        posicao = tabela_mov.index(selecionadas[0])
        movimentacao = sistema.usuario_logado.conta_financeira.movimentacoes[posicao]

        janelinha = ttk.Toplevel(title="Editar movimentação")
        janelinha.configure(background=cor_fundo)
        janelinha.resizable(False, False)
        janelinha.transient(janela)
        janelinha.grab_set()

        quadro = ttk.Frame(janelinha, padding=40)
        quadro.pack(expand=True)

        texto_descricao = ttk.Label(quadro, text="Descrição", font=("Ubuntu", 12))
        texto_descricao.pack(anchor="w")
        campo_descricao = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_descricao.insert(0, movimentacao.descricao)
        campo_descricao.pack(pady=(2, 15), ipady=4)

        texto_valor = ttk.Label(quadro, text="Valor", font=("Ubuntu", 12))
        texto_valor.pack(anchor="w")
        campo_valor = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_valor.insert(0, str(movimentacao.valor))
        campo_valor.pack(pady=(2, 15), ipady=4) 

        texto_data = ttk.Label(quadro, text="Data (DD-MM-AAAA)", font=("Ubuntu", 12))
        texto_data.pack(anchor="w")
        campo_data = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_data.insert(0, movimentacao.data)
        campo_data.pack(pady=(2, 15), ipady=4)

        texto_categoria = ttk.Label(quadro, text="Categoria", font=("Ubuntu", 12))
        texto_categoria.pack(anchor="w")
        categorias = []
        for cat in sistema.usuario_logado.conta_financeira.categorias:
            categorias.append(cat.nome)    
        campo_categoria = ttk.Combobox(quadro, values=categorias, state="readonly", font=("Ubuntu", 12), width=26)
        posicao_categoria_atual = sistema.usuario_logado.conta_financeira.categorias.index(movimentacao.categoria)
        campo_categoria.current(posicao_categoria_atual)
        campo_categoria.pack(pady=(2, 25), ipady=4)

        texto_erro = ttk.Label(quadro, text="", bootstyle="danger", font=("Ubuntu", 11))
        texto_erro.pack(pady=(0, 10))

        def salvar():
            nova_descricao = campo_descricao.get()
            novo_valor = campo_valor.get()
            nova_data = campo_data.get()
            posicao_categoria = campo_categoria.current()
            if nova_descricao == "" or novo_valor == "" or nova_data == "" or posicao_categoria == -1:
                texto_erro.config(text="Preencha todos os campos.")
            else:
                try:
                    novo_valor = float(novo_valor.replace(",", "."))
                except ValueError:
                    texto_erro.config(text="O valor precisa ser um número.")
                    return
                categoria = sistema.usuario_logado.conta_financeira.categorias[posicao_categoria]
                movimentacao.editar_dados(nova_descricao, novo_valor, nova_data, categoria)
                sistema.banco.atualizar_movimentacao(nova_descricao, novo_valor, nova_data, categoria.id, movimentacao.id)
                atualizar_tabela_movimentacoes()
                janelinha.destroy()

        botao_salvar = ttk.Button(quadro, text="Salvar", command=salvar, bootstyle="primary")
        botao_salvar.pack(fill="x", ipady=5)

    botao_editar = ttk.Button(barra_botoes_mov, text="Editar", command=editar_mov, bootstyle="warning")
    botao_editar.pack(side="left", padx=(10, 0), ipady=5, ipadx=15)

    def excluir_mov():
        selecionadas = tabela_mov.selection()
            
        if len(selecionadas) == 0:
            Messagebox.show_warning("Selecione uma movimentação na tabela.", "Atenção")
            return
        
        posicao = tabela_mov.index(selecionadas[0])
        movimentacao = sistema.usuario_logado.conta_financeira.movimentacoes[posicao]
    
        resposta = Messagebox.show_question(
        f"Excluir '{movimentacao.descricao}'?",
        "Confirmar",
        buttons=["Cancelar:secondary", "Excluir:danger"]
        )
    
        if resposta != "Excluir":
            return
                
        sistema.usuario_logado.conta_financeira.excluir_movimentacao(posicao + 1)
        sistema.banco.excluir_movimentacao(movimentacao.id)
        atualizar_tabela_movimentacoes()
    
    botao_excluir = ttk.Button(barra_botoes_mov, text="Excluir", command=excluir_mov, bootstyle="danger-outline")
    botao_excluir.pack(side="left", padx=(10, 0), ipady=5, ipadx=15)


    #------------- Categorias ----------------

    aba_categorias = ttk.Frame(abas, padding=15)
    abas.add(aba_categorias, text="Categorias")

    tabela_cat = ttk.Treeview(aba_categorias, columns=("nome", "descricao"), show="headings")
    tabela_cat.heading("nome", text="Nome", anchor="w")
    tabela_cat.heading("descricao", text="Descrição", anchor="w")
    tabela_cat.tag_configure("impar", background="#f2f4f7")
    tabela_cat.pack(fill="both", expand=True)

    def atualizar_tabela_categorias():
        tabela_cat.delete(*tabela_cat.get_children())
        for i, cat in enumerate(sistema.usuario_logado.conta_financeira.categorias):
            cor = "par" if i % 2 == 0 else "impar"
            tabela_cat.insert("", "end", values=(cat.nome, cat.descricao), tags=(cor,))

    atualizar_tabela_categorias()

    barra_botoes_cat = ttk.Frame(aba_categorias)
    barra_botoes_cat.pack(fill="x", pady=(15, 0))

    def nova_categoria():
        janelinha = ttk.Toplevel(title="Nova categoria")
        janelinha.configure(background=cor_fundo)
        janelinha.resizable(False, False)
        janelinha.transient(janela)
        janelinha.grab_set()

        quadro = ttk.Frame(janelinha, padding=40)
        quadro.pack(expand=True)

        texto_nome = ttk.Label(quadro, text="Nome", font=("Ubuntu", 12))
        texto_nome.pack(anchor="w")
        campo_nome = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_nome.pack(pady=(2, 15), ipady=4)

        texto_descricao = ttk.Label(quadro, text="Descrição", font=("Ubuntu", 12))
        texto_descricao.pack(anchor="w")
        campo_descricao = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_descricao.pack(pady=(2, 25), ipady=4)

        texto_erro = ttk.Label(quadro, text="", bootstyle="danger", font=("Ubuntu", 11))
        texto_erro.pack(pady=(0, 10))

        def salvar():
            nome = campo_nome.get()
            descricao = campo_descricao.get()
            if nome == "" or descricao == "":
                texto_erro.config(text="Preencha todos os campos.")
            else:
                categoria = Categoria(nome, descricao)
                sistema.usuario_logado.conta_financeira.adicionar_categoria(categoria)
                categoria.id = sistema.banco.salvar_categoria(nome, descricao, sistema.usuario_logado.id)
                atualizar_tabela_categorias()
                janelinha.destroy()

        botao_salvar = ttk.Button(quadro, text="Salvar", command=salvar, bootstyle="primary")
        botao_salvar.pack(fill="x", ipady=5)

    botao_adicionar = ttk.Button(barra_botoes_cat, text="+ Adicionar", command=nova_categoria, bootstyle="success")
    botao_adicionar.pack(side="left", ipady=5, ipadx=15)

    def editar_categoria():
        selecionadas = tabela_cat.selection()
        
        if len(selecionadas) == 0:
            Messagebox.show_warning("Selecione uma categoria na tabela.", "Atenção")
            return
    
        posicao = tabela_cat.index(selecionadas[0])
        categoria = sistema.usuario_logado.conta_financeira.categorias[posicao]

        janelinha = ttk.Toplevel(title="Editar categoria")
        janelinha.configure(background=cor_fundo)
        janelinha.resizable(False, False)
        janelinha.transient(janela)
        janelinha.grab_set()
        
        quadro = ttk.Frame(janelinha, padding=40)
        quadro.pack(expand=True)

        texto_nome = ttk.Label(quadro, text="Nome", font=("Ubuntu", 12))
        texto_nome.pack(anchor="w")
        campo_nome = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_nome.insert(0, categoria.nome)
        campo_nome.pack(pady=(2, 15), ipady=4)
        
        
        texto_descricao = ttk.Label(quadro, text="Descrição", font=("Ubuntu", 12))
        texto_descricao.pack(anchor="w")
        campo_descricao = ttk.Entry(quadro, font=("Ubuntu", 12), width=28)
        campo_descricao.insert(0, categoria.descricao)
        campo_descricao.pack(pady=(2, 25), ipady=4)
        
        texto_erro = ttk.Label(quadro, text="", bootstyle="danger", font=("Ubuntu", 11))
        texto_erro.pack(pady=(0, 10))

        def salvar():
            nome = campo_nome.get()
            descricao = campo_descricao.get()
            if nome == "" or descricao == "":
                texto_erro.config(text="Preencha todos os campos.")
            else:
                categoria.alterar_nome(nome)
                categoria.alterar_descricao(descricao)
                sistema.banco.atualizar_categoria(nome, descricao, categoria.id)
                atualizar_tabela_categorias()
                atualizar_tabela_movimentacoes()
                janelinha.destroy()
        
        botao_salvar = ttk.Button(quadro, text="Salvar", command=salvar, bootstyle="primary")
        botao_salvar.pack(fill="x", ipady=5)

    botao_editar = ttk.Button(barra_botoes_cat, text="Editar", command=editar_categoria, bootstyle="warning")
    botao_editar.pack(side="left", padx=(10, 0), ipady=5, ipadx=15)



    #-------------- Resumo --------------
 
    aba_resumo = ttk.Frame(abas, padding=15)
    abas.add(aba_resumo, text="Resumo")

    cartoes = ttk.Frame(aba_resumo)
    cartoes.pack(fill="x", pady=20)
    cartoes.columnconfigure((0, 1, 2), weight=1, uniform="cartao")

    cartao_receitas = ttk.Frame(cartoes, padding=25, bootstyle="success")
    cartao_receitas.grid(row=0, column=0, sticky="nsew", padx=10)
    titulo_receitas = ttk.Label(cartao_receitas, text="Receitas", font=("Ubuntu", 14), bootstyle="inverse-success")
    titulo_receitas.pack(anchor="w")
    valor_receitas = ttk.Label(cartao_receitas, text="R$ 0.00", font=("Ubuntu", 24, "bold"), bootstyle="inverse-success")
    valor_receitas.pack(anchor="w", pady=(10, 0))

    cartao_despesas = ttk.Frame(cartoes, padding=25, bootstyle="danger")
    cartao_despesas.grid(row=0, column=1, sticky="nsew", padx=10)
    titulo_despesas = ttk.Label(cartao_despesas, text="Despesas", font=("Ubuntu", 14), bootstyle="inverse-danger")
    titulo_despesas.pack(anchor="w")
    valor_despesas = ttk.Label(cartao_despesas, text="R$ 0.00", font=("Ubuntu", 24, "bold"), bootstyle="inverse-danger")
    valor_despesas.pack(anchor="w", pady=(10, 0))

    cartao_saldo_atual = ttk.Frame(cartoes, padding=25, bootstyle="primary")
    cartao_saldo_atual.grid(row=0, column=2, sticky="nsew", padx=10)
    titulo_saldo_atual = ttk.Label(cartao_saldo_atual, text="Saldo Atual", font=("Ubuntu", 14), bootstyle="inverse-primary")
    titulo_saldo_atual.pack(anchor="w")
    valor_saldo_atual = ttk.Label(cartao_saldo_atual, text="R$ 0.00", font=("Ubuntu", 24, "bold"), bootstyle="inverse-primary")
    valor_saldo_atual.pack(anchor="w", pady=(10, 0))

    barra_saldo = ttk.Frame(aba_resumo)
    barra_saldo.pack(fill="x", pady=(15, 0))
    
    titulo_saldo_inicial = ttk.Label(barra_saldo, text="Saldo Inicial:", font=("Ubuntu", 14))
    titulo_saldo_inicial.pack(side="left")
    valor_saldo_inicial = ttk.Label(barra_saldo, text="R$ 0.00", font=("Ubuntu", 14))
    valor_saldo_inicial.pack(side="left", padx=(5, 0))

    def atualizar_resumo():
        resumo = ResumoFinanceiro()
        resumo.calcular_resumo(sistema.usuario_logado.conta_financeira.saldo_inicial, sistema.usuario_logado.conta_financeira.movimentacoes)
        valor_receitas.config(text=f"R$ {resumo.total_receitas:.2f}")
        valor_despesas.config(text=f"R$ {resumo.total_despesas:.2f}")
        valor_saldo_atual.config(text=f"R$ {resumo.saldo_atual:.2f}")
        valor_saldo_inicial.config(text=f"R$ {sistema.usuario_logado.conta_financeira.saldo_inicial:.2f}")

    atualizar_resumo()
    abas.bind("<<NotebookTabChanged>>", lambda evento: atualizar_resumo())

    def atualizar_saldo_inicial():
        janela_saldo = ttk.Toplevel(title="Saldo Inicial")
        janela_saldo.configure(background=cor_fundo)
        janela_saldo.resizable(False, False)
        janela_saldo.transient(janela)
        janela_saldo.grab_set()

        quadro_saldo = ttk.Frame(janela_saldo, padding=30)
        quadro_saldo.pack(fill="both", expand=True)

        ttk.Label(quadro_saldo, text="Novo valor (R$)", font=("Ubuntu", 12)).pack(anchor="w")
        campo_saldo = ttk.Entry(quadro_saldo, font=("Ubuntu", 14), width=25)
        campo_saldo.insert(0, f"{sistema.usuario_logado.conta_financeira.saldo_inicial:.2f}")
        campo_saldo.pack(fill="x", pady=(5, 5), ipady=4)

        texto_erro = ttk.Label(quadro_saldo, text="", bootstyle="danger")
        texto_erro.pack(anchor="w", pady=(0, 15))

        def salvar():
            try:
                novo_saldo = float(campo_saldo.get().replace(",", "."))
            except ValueError:
                texto_erro.config(text="Digite um número válido.")
                return
            sistema.usuario_logado.conta_financeira.definir_saldo_inicial(novo_saldo)
            sistema.banco.atualizar_saldo_inicial(sistema.usuario_logado.id, novo_saldo)
            atualizar_resumo()
            janela_saldo.destroy()

        botoes_saldo = ttk.Frame(quadro_saldo)
        botoes_saldo.pack(fill="x")
        ttk.Button(botoes_saldo, text="Cancelar", bootstyle="secondary-outline", command=janela_saldo.destroy).pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=5)
        ttk.Button(botoes_saldo, text="Salvar", bootstyle="primary", command=salvar).pack(side="left", expand=True, fill="x", padx=(5, 0), ipady=5)

    botao_atualizar_saldo = ttk.Button(barra_saldo, text="Alterar", command=atualizar_saldo_inicial, bootstyle="primary-outline")
    botao_atualizar_saldo.pack(side="left", padx=(10, 0), ipady=5, ipadx=15)


        

mostrar_login()
janela.mainloop()