"""
TaskTracker - Sistema de gerenciamento de tarefas via linha de comando.

Implementa a Fase 2 do projeto cumulativo do Bootcamp II: traduz em
código Python a receita lógica desenhada na Fase 1 (planejamento em
docs/planejamento_logico.pdf).
"""

import json
import os
from datetime import date, datetime

CAMINHO_DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tarefas.json")


# ---------------------------------------------------------------------------
# Persistência (R8: toda alteração é gravada antes de voltar ao menu)
# ---------------------------------------------------------------------------

def carregar_tarefas():
    """Lê o arquivo de dados. Se não existir ou estiver corrompido, devolve lista vazia."""
    if not os.path.exists(CAMINHO_DADOS):
        return []
    try:
        with open(CAMINHO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        print("Aviso: o arquivo de dados está corrompido ou ilegível. Iniciando com lista vazia.")
        return []


def gravar_tarefas(tarefas):
    """Grava a lista de tarefas no arquivo de dados, substituindo a versão anterior."""
    os.makedirs(os.path.dirname(CAMINHO_DADOS), exist_ok=True)
    with open(CAMINHO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Operações do menu (seções 3.2 e 3.3 da receita lógica)
# ---------------------------------------------------------------------------

def proximo_id(tarefas):
    """R4: ID numérico único, nunca reaproveitado."""
    if not tarefas:
        return 1
    return max(tarefa["id"] for tarefa in tarefas) + 1


def cadastrar_tarefa(tarefas):
    print("\n--- Cadastrar nova tarefa ---")
    titulo = input("Título da tarefa: ").strip()
    descricao = input("Descrição (opcional): ").strip()
    prioridade = input("Prioridade (Alta, Média, Baixa): ").strip()
    data_limite = input("Data limite (DD/MM/AAAA): ").strip()

    tarefa = {
        "id": proximo_id(tarefas),
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "data_limite": data_limite,
        "status": "Pendente",
    }
    tarefas.append(tarefa)
    gravar_tarefas(tarefas)
    print(f"\nTarefa cadastrada com sucesso. ID: {tarefa['id']}\n")


def visualizar_tarefas(tarefas):
    print("\n--- Tarefas cadastradas ---")
    if not tarefas:
        print("Ainda não há tarefas cadastradas.\n")
        return

    print(f"{'ID':<4}{'Título':<30}{'Prioridade':<12}{'Data limite':<14}{'Status':<12}")
    print("-" * 72)
    for tarefa in tarefas:
        print(
            f"{tarefa['id']:<4}{tarefa['titulo'][:28]:<30}{tarefa['prioridade']:<12}"
            f"{tarefa['data_limite']:<14}{tarefa['status']:<12}"
        )

    total = len(tarefas)
    pendentes = sum(1 for tarefa in tarefas if tarefa["status"] == "Pendente")
    concluidas = total - pendentes
    print("-" * 72)
    print(f"Total: {total} | Pendentes: {pendentes} | Concluídas: {concluidas}\n")


# ---------------------------------------------------------------------------
# Menu principal (seção 3.1 da receita lógica)
# ---------------------------------------------------------------------------

def exibir_menu():
    print("=" * 40)
    print("          TASKTRACKER")
    print("=" * 40)
    print("1. Cadastrar nova tarefa")
    print("2. Visualizar tarefas cadastradas")
    print("3. Sair da aplicação")


def main():
    tarefas = carregar_tarefas()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_tarefa(tarefas)
        elif opcao == "2":
            visualizar_tarefas(tarefas)
        elif opcao == "3":
            gravar_tarefas(tarefas)
            print("\nDados salvos. Até a próxima!")
            break
        else:
            print("\nOpção inválida. Escolha um número de 1 a 3.\n")


if __name__ == "__main__":
    main()
