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
PRIORIDADES_VALIDAS = {"alta": "Alta", "media": "Média", "média": "Média", "baixa": "Baixa"}


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
# Validações (R1, R2, R3 do planejamento da Fase 1)
# ---------------------------------------------------------------------------

def pedir_titulo():
    """R1: título obrigatório, não vazio, não só espaços."""
    while True:
        titulo = input("Título da tarefa: ").strip()
        if titulo:
            return titulo
        print("O título não pode ficar em branco. Tente novamente.\n")


def pedir_prioridade():
    """R2: só aceita Alta, Média ou Baixa, sem diferenciar maiúsculas de minúsculas."""
    while True:
        bruta = input("Prioridade (Alta, Média, Baixa): ").strip().lower()
        if bruta in PRIORIDADES_VALIDAS:
            return PRIORIDADES_VALIDAS[bruta]
        print("Prioridade inválida. Use Alta, Média ou Baixa.\n")


def pedir_data_limite():
    """R3: formato DD/MM/AAAA, data existente, não anterior a hoje."""
    while True:
        bruta = input("Data limite (DD/MM/AAAA): ").strip()
        try:
            data_informada = datetime.strptime(bruta, "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use o formato DD/MM/AAAA com uma data real.\n")
            continue
        if data_informada < date.today():
            print("A data limite não pode ser anterior a hoje.\n")
            continue
        return bruta


# ---------------------------------------------------------------------------
# Operações do menu (seções 3.2 a 3.5 da receita lógica)
# ---------------------------------------------------------------------------

def proximo_id(tarefas):
    """R4: ID numérico único, nunca reaproveitado."""
    if not tarefas:
        return 1
    return max(tarefa["id"] for tarefa in tarefas) + 1


def cadastrar_tarefa(tarefas):
    print("\n--- Cadastrar nova tarefa ---")
    titulo = pedir_titulo()
    descricao = input("Descrição (opcional): ").strip()
    prioridade = pedir_prioridade()
    data_limite = pedir_data_limite()

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

    ordem_prioridade = {"Alta": 0, "Média": 1, "Baixa": 2}

    def chave_ordenacao(tarefa):
        data_ordenavel = datetime.strptime(tarefa["data_limite"], "%d/%m/%Y").date()
        return (ordem_prioridade[tarefa["prioridade"]], data_ordenavel)

    tarefas_ordenadas = sorted(tarefas, key=chave_ordenacao)
    hoje = date.today()

    print(f"{'ID':<4}{'Título':<30}{'Prioridade':<12}{'Data limite':<14}{'Status':<12}")
    print("-" * 72)
    for tarefa in tarefas_ordenadas:
        data_tarefa = datetime.strptime(tarefa["data_limite"], "%d/%m/%Y").date()
        atrasada = tarefa["status"] == "Pendente" and data_tarefa < hoje
        marcador = " [ATRASADA]" if atrasada else ""
        print(
            f"{tarefa['id']:<4}{tarefa['titulo'][:28]:<30}{tarefa['prioridade']:<12}"
            f"{tarefa['data_limite']:<14}{tarefa['status']:<12}{marcador}"
        )

    total = len(tarefas)
    pendentes = sum(1 for tarefa in tarefas if tarefa["status"] == "Pendente")
    concluidas = total - pendentes
    print("-" * 72)
    print(f"Total: {total} | Pendentes: {pendentes} | Concluídas: {concluidas}\n")


def concluir_tarefa(tarefas):
    print("\n--- Concluir tarefa ---")
    if not tarefas:
        print("Não há tarefas cadastradas.\n")
        return

    visualizar_tarefas(tarefas)
    try:
        id_informado = int(input("ID da tarefa a concluir: ").strip())
    except ValueError:
        print("ID inválido.\n")
        return

    for tarefa in tarefas:
        if tarefa["id"] == id_informado:
            if tarefa["status"] == "Concluída":
                print("Essa tarefa já está concluída.\n")
                return
            tarefa["status"] = "Concluída"
            gravar_tarefas(tarefas)
            print(f"Tarefa '{tarefa['titulo']}' marcada como concluída.\n")
            return

    print("Não existe tarefa com esse ID.\n")


def excluir_tarefa(tarefas):
    print("\n--- Excluir tarefa ---")
    if not tarefas:
        print("Não há tarefas cadastradas.\n")
        return

    visualizar_tarefas(tarefas)
    try:
        id_informado = int(input("ID da tarefa a excluir: ").strip())
    except ValueError:
        print("ID inválido.\n")
        return

    for tarefa in tarefas:
        if tarefa["id"] == id_informado:
            confirmacao = input(f"Confirma a exclusão de '{tarefa['titulo']}'? (S/N): ").strip().upper()
            if confirmacao != "S":
                print("Exclusão cancelada.\n")
                return
            tarefas.remove(tarefa)
            gravar_tarefas(tarefas)
            print("Tarefa excluída com sucesso.\n")
            return

    print("Não existe tarefa com esse ID.\n")


# ---------------------------------------------------------------------------
# Menu principal (seção 3.1 da receita lógica)
# ---------------------------------------------------------------------------

def exibir_menu():
    print("=" * 40)
    print("          TASKTRACKER")
    print("=" * 40)
    print("1. Cadastrar nova tarefa")
    print("2. Visualizar tarefas cadastradas")
    print("3. Concluir tarefa")
    print("4. Excluir tarefa")
    print("5. Sair da aplicação")


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
            concluir_tarefa(tarefas)
        elif opcao == "4":
            excluir_tarefa(tarefas)
        elif opcao == "5":
            gravar_tarefas(tarefas)
            print("\nDados salvos. Até a próxima!")
            break
        else:
            print("\nOpção inválida. Escolha um número de 1 a 5.\n")


if __name__ == "__main__":
    main()
