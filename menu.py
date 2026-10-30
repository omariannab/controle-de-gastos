import os
from models.sistema import SistemaControleGastos
from models.categoria import Categoria
from models.movimentacao import Receita, Despesa
from models.resumo_financeiro import ResumoFinanceiro

sistema = SistemaControleGastos()

def menu_conta():
    conta = sistema.usuario_logado.conta_financeira

    while True:
  
        os.system("clear")  
        print(f"=== Olá, {sistema.usuario_logado.nome} ===")
        print("1. Definir saldo inicial")
        print("2. Adicionar categoria")
        print("3. Listar categorias")
        print("4. Editar categoria")
        print("5. Registrar receita")
        print("6. Registrar despesa")
        print("7. Listar movimentações")
        print("8. Editar movimentação")
        print("9. Excluir movimentação")
        print("10. Resumo financeiro")
        print("11. Ver saldo")
        print("12. Ver meus dados")
        print("0. Sair da conta")
        esc = input("Escolha uma opção: ")

        try:
            if esc == "1":
                saldo_inicial = float(input("Insira o saldo inicial da conta: "))
                conta.definir_saldo_inicial(saldo_inicial)
                sistema.banco.atualizar_saldo_inicial(sistema.usuario_logado.id, saldo_inicial)
            elif esc == "2":
                nome_categoria = input("Insira o nome da categoria: ")
                descricao = input("Descrição: ")
                categoria = Categoria(nome_categoria, descricao)
                conta.adicionar_categoria(categoria)
                categoria.id = sistema.banco.salvar_categoria(nome_categoria, descricao, sistema.usuario_logado.id)
            elif esc == "3":
                for i, c in enumerate(conta.categorias):
                    print(f"{i + 1}.", end=" ")
                    c.mostrar_dados()
            elif esc == "4":
                            for i, c in enumerate(conta.categorias):
                                print(f"{i + 1}.", end=" ")
                                c.mostrar_dados()
                            index = int(input("Insira o índice da categoria que deseja editar: ")) - 1
                            categoria = conta.categorias[index]
                            novo_nome = input("Novo nome da categoria: ")
                            nova_descricao = input("Nova descrição da categoria: ")
                            categoria.alterar_nome(novo_nome)
                            categoria.alterar_descricao(nova_descricao)
                            sistema.banco.atualizar_categoria(novo_nome, nova_descricao, categoria.id)
            elif esc == "5":
                nome_receita = input("Insira o nome da receita:")
                valor = float(input("Insira o valor da receita: "))
                data = input("Insira a data da receita (dd/mm/aaaa): ")
                for i, c in enumerate(conta.categorias):
                    print(f"{i + 1}.", end=" ")
                    c.mostrar_dados()
                categoria_index = int(input("Escolha a categoria da receita (número): ")) - 1
                categoria = conta.categorias[categoria_index]
                receita = Receita(nome_receita, valor, data, categoria)
                conta.adicionar_movimentacao(receita)
                receita.id = sistema.banco.salvar_movimentacao("receita", nome_receita, valor, data, categoria.id, sistema.usuario_logado.id)
            elif esc == "6":
                nome_despesa = input("Insira o nome da despesa: ")
                valor = float(input("Insira o valor da despesa: "))
                data = input("Insira a data da despesa (dd/mm/aaaa): ")
                for i, c in enumerate(conta.categorias):
                    print(f"{i + 1}.", end=" ")
                    c.mostrar_dados()
                categoria_index = int(input("Escolha a categoria da despesa (número): ")) - 1
                categoria = conta.categorias[categoria_index]
                despesa = Despesa(nome_despesa, valor, data, categoria)
                conta.adicionar_movimentacao(despesa)
                despesa.id = sistema.banco.salvar_movimentacao("despesa", nome_despesa, valor, data, categoria.id, sistema.usuario_logado.id)
            elif esc == "7":    
                conta.listar_movimentacoes()
            elif esc == "8":
                            conta.listar_movimentacoes() 
                            index = int(input("Insira o índice da movimentação que deseja editar: "))
                            nova_descricao = input("Nova descrição: ")
                            novo_valor = float(input("Novo valor: "))
                            nova_data = input("Nova data (dd/mm/aaaa): ")
                            for i, c in enumerate(conta.categorias):
                                print(f"{i + 1}.", end=" ")
                                c.mostrar_dados()
                            categoria_index = int(input("Escolha a nova categoria (número): ")) - 1
                            nova_categoria = conta.categorias[categoria_index]
                            conta.editar_movimentacao(index, nova_descricao, novo_valor, nova_data, nova_categoria)
                            movimentacao = conta.movimentacoes[index - 1]
                            sistema.banco.atualizar_movimentacao(nova_descricao, novo_valor, nova_data, nova_categoria.id, movimentacao.id)
            elif esc == "9":
                conta.listar_movimentacoes()
                index = int(input("Insira o índice da movimentação que deseja excluir: ")) 
                movimentacao = conta.movimentacoes[index-1]
                sistema.banco.excluir_movimentacao(movimentacao.id)
                conta.excluir_movimentacao(index)
            elif esc == "10":
                resumo = ResumoFinanceiro()
                resumo.calcular_resumo(conta.saldo_inicial, conta.movimentacoes)
                resumo.mostrar_resumo()
            elif esc == "11":
                conta.calcular_saldo()
                print(f"Saldo atual: {conta.calcular_saldo()}")
            elif esc == "12":
                sistema.usuario_logado.mostrar_dados()
            elif esc == "0":
                sistema.encerrar_sessao()
                break
            else:
                print("Opção inválida!")
        except ValueError:
            print("Valor inválido! Digite um número.")
        except IndexError:
            print("Número não encontrado na lista.")
        input("\nPressione Enter para continuar...")  

while True:
    os.system("clear")  
    print("1. Cadastrar usuário")
    print("2. Login")
    print("0. Sair")
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        nome = input("Nome: ")
        usuario = input("Nome do novo usuário: ")
        senha = input("Senha: ")
        sistema.cadastrar_usuario(nome, usuario, senha)
    elif escolha == "2":
        usuario = input("Nome do usuário: ")
        senha = input("Senha: ")
        if sistema.realizar_login(usuario, senha):
            menu_conta()
    elif escolha == "0":
        break
    else:
        print("Opção inválida")
    input("\nPressione Enter para continuar...") 

