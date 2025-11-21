from tarefas import (
    criar_tarefa, verificar_urgencia, atualizar_prioridade,
    concluir_tarefa, arquivar_tarefas, excluir_tarefa,
    relatorio_tarefas, relatorio_arquivados
)


def safe_int_input(prompt: str) -> int:
    val = input(prompt)
    try:
        return int(val)
    except ValueError:
        raise ValueError("Entrada deve ser um número inteiro.")


def menu():
    while True:
        print("""
=========== MENU ===========
1. Criar tarefa
2. Ver urgentes
3. Atualizar prioridade
4. Concluir tarefa
5. Arquivar tarefas (padrão: 7 dias)
6. Excluir tarefa
7. Relatório de tarefas
8. Relatório arquivados
9. Sair
""")
        opcao = input("Escolha: ").strip()

        if opcao == '1':
            titulo = input("Título: ").strip()
            descricao = input("Descrição (opcional): ").strip()
            prioridade = input("Prioridade (Urgente, Alta, Média, Baixa): ").strip()
            origem = input("Origem (E-mail, Telefone, Chamado do Sistema): ").strip()
            criar_tarefa(titulo, descricao, prioridade, origem)

        elif opcao == '2':
            verificar_urgencia()

        elif opcao == '3':
            try:
                id_tarefa = safe_int_input("ID da tarefa: ")
            except ValueError as e:
                print(e)
                continue
            nova = input("Nova prioridade: ").strip()
            atualizar_prioridade(id_tarefa, nova)

        elif opcao == '4':
            try:
                id_tarefa = safe_int_input("ID da tarefa: ")
            except ValueError as e:
                print(e)
                continue
            concluir_tarefa(id_tarefa)

        elif opcao == '5':
            dias = input("Arquivar tarefas concluídas há mais de quantos dias? (enter = 7): ").strip()
            try:
                dias_int = int(dias) if dias else 7
            except ValueError:
                print("Entrada inválida, usando 7 dias.")
                dias_int = 7
            arquivar_tarefas(dias_int)

        elif opcao == '6':
            try:
                id_tarefa = safe_int_input("ID da tarefa: ")
            except ValueError as e:
                print(e)
                continue
            excluir_tarefa(id_tarefa)

        elif opcao == '7':
            relatorio_tarefas()

        elif opcao == '8':
            relatorio_arquivados()

        elif opcao == '9':
            print("Saindo...")
            break

        else:
            print("Opção inválida.")
