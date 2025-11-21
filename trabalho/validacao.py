from typing import Optional

# Definições "canônicas" — a validação usa formas canônicas internalmente.
PRIORIDADES = {
    "urgente": "Urgente",
    "alta": "Alta",
    "media": "Média",
    "média": "Média",
    "baixa": "Baixa"
}

ORIGENS = {
    "e-mail": "E-mail",
    "email": "E-mail",
    "telefone": "Telefone",
    "chamado do sistema": "Chamado do Sistema",
    "chamado": "Chamado do Sistema",
    "sistema": "Chamado do Sistema"
}

STATUS_VALIDOS = {"Pendente", "Fazendo", "Concluída", "Arquivado", "Excluída"}


def normalizar_string(s: str) -> str:
    return (s or "").strip().lower()


def validar_e_normalizar_prioridade(prioridade: str) -> Optional[str]:
    """
    Retorna a forma canônica (ex: "Urgente") ou None se inválido.
    Aceita variações case-insensitive e alguns sinônimos básicos.
    """
    chave = normalizar_string(prioridade)
    return PRIORIDADES.get(chave)


def validar_e_normalizar_origem(origem: str) -> Optional[str]:
    chave = normalizar_string(origem)
    return ORIGENS.get(chave)


def validar_status(status: str) -> bool:
    return (status or "").strip() in STATUS_VALIDOS
