import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

BASE_DIR = Path(__file__).parent
TAREFAS_FILE = BASE_DIR / "tarefas.json"
ARQUIVADAS_FILE = BASE_DIR / "tarefas_arquivadas.json"


class DataStore:
    def __init__(self, tarefas_file: Path = TAREFAS_FILE, arquivadas_file: Path = ARQUIVADAS_FILE):
        self.tarefas_file = tarefas_file
        self.arquivadas_file = arquivadas_file
        self.tarefas: List[Dict] = []
        self.tarefas_arquivadas: List[Dict] = []
        self._id_counter: int = 1

    def carregar_dados(self) -> None:
        try:
            if self.tarefas_file.exists():
                with open(self.tarefas_file, "r", encoding="utf-8") as f:
                    self.tarefas = json.load(f)
            else:
                self.tarefas = []

            if self.arquivadas_file.exists():
                with open(self.arquivadas_file, "r", encoding="utf-8") as f:
                    self.tarefas_arquivadas = json.load(f)
            else:
                self.tarefas_arquivadas = []

            # recalcula id
            all_ids = [t.get("id", 0) for t in (self.tarefas + self.tarefas_arquivadas)]
            if all_ids:
                self._id_counter = max(all_ids) + 1
            else:
                self._id_counter = 1

            print("Dados carregados.")
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.tarefas = []
            self.tarefas_arquivadas = []
            self._id_counter = 1

    def salvar_dados(self) -> None:
        try:
            with open(self.tarefas_file, "w", encoding="utf-8") as f:
                json.dump(self.tarefas, f, ensure_ascii=False, indent=4)

            with open(self.arquivadas_file, "w", encoding="utf-8") as f:
                json.dump(self.tarefas_arquivadas, f, ensure_ascii=False, indent=4)

            print("Dados salvos.")
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def next_id(self) -> int:
        nid = self._id_counter
        self._id_counter += 1
        return nid

    # --- operações de alto nível sobre tarefas ---
    def adicionar_tarefa(self, tarefa: Dict) -> None:
        self.tarefas.append(tarefa)
        self.salvar_dados()

    def atualizar_tarefa(self, id_tarefa: int, atualizacao: Dict) -> bool:
        for t in self.tarefas:
            if t.get("id") == id_tarefa:
                t.update(atualizacao)
                self.salvar_dados()
                return True
        return False

    def concluir_tarefa(self, id_tarefa: int) -> bool:
        for t in self.tarefas:
            if t.get("id") == id_tarefa:
                t["status"] = "Concluída"
                t["data_conclusao"] = datetime.now().isoformat()
                self.salvar_dados()
                return True
        return False

    def excluir_tarefa(self, id_tarefa: int) -> bool:
        for t in list(self.tarefas):
            if t.get("id") == id_tarefa:
                t["status"] = "Excluída"
                self.tarefas.remove(t)
                self.tarefas_arquivadas.append(t)
                self.salvar_dados()
                return True
        return False

    def arquivar_tarefas_anteriores_a(self, dias: int = 7) -> int:
        from datetime import datetime, timedelta

        agora = datetime.now()
        mover = []

        for t in list(self.tarefas):
            if t.get("status") == "Concluída" and t.get("data_conclusao"):
                try:
                    dt = datetime.fromisoformat(t["data_conclusao"])
                except Exception:
                    # se data estiver inválida, pule
                    continue
                if agora - dt > timedelta(days=dias):
                    t["status"] = "Arquivado"
                    mover.append(t)

        for t in mover:
            if t in self.tarefas:
                self.tarefas.remove(t)
                self.tarefas_arquivadas.append(t)

        if mover:
            self.salvar_dados()
        return len(mover)

    def buscar_tarefa(self, id_tarefa: int) -> Optional[Dict]:
        for t in self.tarefas:
            if t.get("id") == id_tarefa:
                return t
        return None

    def listar_urgentes(self) -> List[Dict]:
        return [t for t in self.tarefas if t.get("prioridade") == "Urgente"]

    def todas_tarefas(self) -> List[Dict]:
        return list(self.tarefas)

    def todas_arquivadas(self) -> List[Dict]:
        return list(self.tarefas_arquivadas)


# instância a ser importada pelos outros módulos
store = DataStore()
