from models.movimentacao import Receita, Despesa
from models.categoria import Categoria
from models.resumo_financeiro import ResumoFinanceiro
from models.sistema import SistemaControleGastos

print("----- 1. Cadastrar usuários -----")
sistema = SistemaControleGastos()
sistema.cadastrar_usuario("Marianna", "marianna", "123456")
print(sistema.cadastrar_usuario("Alice", "marianna", "123456")) #Deve mostrar erro de username repetido
sistema.cadastrar_usuario("Alice", "alice", "123456")
print(f"Total de usuários cadastrados: {len(sistema.usuarios)}")  #Deve mostrar 2 usuários cadastrados

print("----- 2. Login (um com senha errada, um com senha certa) -----")

sistema.realizar_login("marianna", "senha_errada")  #Deve falhar
sistema.realizar_login("marianna", "123456")  #Deve funcionar
sistema.usuario_logado.mostrar_dados()  #Deve mostrar os dados do usuário logado    

print("----- 3. Definir saldo inicial -----")

conta = sistema.usuario_logado.conta_financeira
conta.definir_saldo_inicial(1000)
print(f"Saldo inicial definido para {sistema.usuario_logado.nome}: {conta.saldo_inicial}")  #Deve mostrar 1000

print("----- 4. Criar categorias e adicionar na conta -----")

renda = Categoria("Renda", "Receitas provenientes de salário, freelances, investimentos, etc.")
alimentacao = Categoria("Alimentação", "Despesas com alimentação, como supermercado, restaurantes, delivery, etc.")
moradia = Categoria("Moradia", "Despesas com aluguel, condomínio, manutenção da casa, etc.")

conta.adicionar_categoria(renda)
conta.adicionar_categoria(alimentacao)
conta.adicionar_categoria(moradia)
print(f"Categorias na conta: {len(conta.categorias)}") #Deve mostrar 3 categorias

renda.mostrar_dados()

renda.alterar_nome("Renda Mensal")
renda.mostrar_dados()

renda.alterar_descricao("Salário, freelances, investimentos e outras fontes de renda.")
renda.mostrar_dados()

print("----- 5. Registrar receitas e despesas -----")

salario = Receita("Salário", 3000, "22/10/2026", renda)
aluguel = Despesa("Aluguel", 1200, "01/10/2026", moradia)
mercado = Despesa("Mercado", 400, "05/10/2026", alimentacao)

conta.adicionar_movimentacao(salario)
conta.adicionar_movimentacao(aluguel)
conta.adicionar_movimentacao(mercado)
print(f"Total de movimentações registradas: {len(conta.movimentacoes)}")  #Deve mostrar 3 movimentações

print(salario.efeito_no_saldo())   # 3000
print(aluguel.efeito_no_saldo())   # -1200
print(mercado.efeito_no_saldo())   # -400

print("----- 6. Listar, editar e excluir movimentações -----")

conta.listar_movimentacoes()  #Deve listar as 3 movimentações
print("---")
conta.editar_movimentacao(3, "Supermercado", 450, "06/10/2026", alimentacao)  #Editando a movimentação de índice 3
conta.listar_movimentacoes()  #Deve listar as movimentações com a alteração
print("---")
conta.excluir_movimentacao(2)  #Excluindo a movimentação de índice 2            
conta.listar_movimentacoes()  #Deve listar as movimentações

print("----- 7. Resumo financeiro e calcular_saldo -----")

resumo = ResumoFinanceiro()
resumo.calcular_resumo(conta.saldo_inicial, conta.movimentacoes)
resumo.mostrar_resumo()  #Deve mostrar o resumo financeiro com total de receitas, total de despesas e saldo atual
print(f"Saldo pela conta: {conta.calcular_saldo()}")

print("----- 8. Encerrar sessão -----")

sistema.encerrar_sessao()
print(f"Usuário logado: {sistema.usuario_logado}")
