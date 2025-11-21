from datetime import datetime
from typing import Optional
from persistencia import store
from validacao import validar_e_normalizar_prioridade, validar_e_normalizar_origem


def criar_tarefa(titulo: str, descricao: str, prioridade: str, origem: str) -> Optional[int]:
    if not titulo or not prioridade or not origem:
        print("Erro: Título, prioridade e origem são obrigatórios.")
        return None

    prioridade_norm = validar_e_normalizar_prioridade(prioridade)
    origem_norm = validar_e_normalizar_origem(origem)

    if not prioridade_norm:
        print(f"Erro: prioridade inválida: '{prioridade}'. Opções: Urgente, Alta, Média, Baixa.")
        return None

    if not origem_norm:
        print(f"Erro: origem inválida: '{origem}'. Opções: E-mail, Telefone, Chamado do Sistema.")
        return None

    tarefa = {
        "id": store.next_id(),
        "titulo": titulo.strip(),
        "descricao": (descricao or "").strip(),
        "prioridade": prioridade_norm,
        "status": "Pendente",
        "origem": origem_norm,
        "data_criacao": datetime.now().isoformat(),
        "data_conclusao": None
    }

    store.adicionar_tarefa(tarefa)
    print(f"Tarefa criada com ID {tarefa['id']}")
    return tarefa["id"]


def verificar_urgencia():
    urgentes = store.listar_urgentes()
    if not urgentes:
        print("Nenhuma tarefa urgente.")
        return
    print("\nTarefas URGENTES:")
    for t in urgentes:
        print(f"ID: {t['id']} | Título: {t['titulo']} | Status: {t['status']}")


def atualizar_prioridade(id_tarefa: int, nova_prioridade: str):
    prioridade_norm = validar_e_normalizar_prioridade(nova_prioridade)
    if not prioridade_norm:
        print("Prioridade inválida.")
        return

    ok = store.atualizar_tarefa(id_tarefa, {"prioridade": prioridade_norm})
    if ok:
        print("Prioridade atualizada.")
    else:
        print("Tarefa não encontrada.")


def concluir_tarefa(id_tarefa: int):
    ok = store.concluir_tarefa(id_tarefa)
    if ok:
        print("Tarefa concluída.")
    else:
        print("Tarefa não encontrada.")


def arquivar_tarefas(dias: int = 7):
    qtd = store.arquivar_tarefas_anteriores_a(dias)
    print(f"{qtd} tarefas arquivadas.")


def excluir_tarefa(id_tarefa: int):
    ok = store.excluir_tarefa(id_tarefa)
    if ok:
        print("Tarefa excluída e movida para arquivadas.")
    else:
        print("Tarefa não encontrada.")


def relatorio_tarefas():
    tarefas = store.todas_tarefas()
    if not tarefas:
        print("Nenhuma tarefa ativa.")
        return

    print("\nRELATÓRIO DE TAREFAS:")
    for t in tarefas:
        print(f"ID: {t['id']} | Título: {t['titulo']} | Prioridade: {t['prioridade']} | Status: {t['status']}")
        if t.get("descricao"):
            print(f"Descrição: {t['descricao']}")
        print(f"Criada em: {t['data_criacao']}")
        if t["status"] == "Concluída" and t.get("data_conclusao"):
            try:
                dt_c = datetime.fromisoformat(t["data_conclusao"])
                dt_i = datetime.fromisoformat(t["data_criacao"])
                print(f"Tempo de execução: {dt_c - dt_i}")
            except Exception:
                pass
        print("-" * 40)


def relatorio_arquivados():
    arquivadas = store.todas_arquivadas()
    if not arquivadas:
        print("Nenhuma tarefa arquivada/excluída.")
        return

    print("\nARQUIVADOS:")
    for t in arquivadas:
        print(f"ID: {t['id']} | Título: {t['titulo']} | Status: {t['status']} | Origem: {t.get('origem')}")
