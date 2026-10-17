# TaskTracker

Sistema de gerenciamento de tarefas via linha de comando, escrito em Python. Projeto cumulativo do Bootcamp II (CEUB) esta é a Fase 2 (Entrega Intermediária), que implementa em código a lógica planejada na Fase 1.

## O que o sistema faz

- Cadastra tarefas com título, descrição, prioridade (Alta, Média, Baixa) e data limite.
- Valida cada entrada antes de aceitar: título não pode ficar vazio, prioridade só aceita os três valores definidos, data precisa ser real e não pode estar no passado.
- Lista as tarefas ordenadas por prioridade e data limite, com total de pendentes e concluídas.
- Conclui uma tarefa sem apagá-la, mantendo histórico.
- Exclui uma tarefa mediante confirmação explícita.
- Persiste tudo em `data/tarefas.json`: fechar o programa não perde nada.

## Estrutura do projeto

```
tasktracker-projeto/
├── README.md                    # Este arquivo
├── .gitignore                   # Arquivos ignorados pelo versionamento
├── requirements.txt             # Dependências do projeto (nenhuma nesta fase)
├── docs/
│   └── planejamento_logico.pdf  # Planejamento lógico da Fase 1
├── data/
│   └── tarefas.json             # Base de dados local, gerada em tempo de execução
└── src/
    └── main.py                  # Código-fonte da aplicação
```

## Como executar

Requer Python 3.8 ou superior. Nenhuma dependência externa é necessária.

```bash
git clone <url-do-repositorio>
cd tasktracker-projeto
python3 src/main.py
```

O arquivo `data/tarefas.json` é criado automaticamente no primeiro cadastro.

## Regras de negócio implementadas

| Regra | Descrição |
|---|---|
| R1 | Título obrigatório; vazio ou só espaços é recusado. |
| R2 | Prioridade restrita a Alta, Média ou Baixa. |
| R3 | Data limite precisa existir no calendário e não pode ser anterior a hoje. |
| R4 | ID numérico único, nunca reaproveitado após exclusão. |
| R5 | Toda tarefa nasce Pendente; única transição é para Concluída. |
| R6 | Concluir não remove a tarefa fica registrada para histórico. |
| R7 | Exclusão exige confirmação explícita do usuário. |
| R8 | Toda alteração é gravada em disco antes de voltar ao menu. |
| R9 | Entrada inválida nunca derruba o programa. |

## Próximos passos (Fase 3)

Containerização da aplicação com Docker, testes automatizados e empacotamento para deploy.

## Autor

Rafael Robson Nunes de Araújo — Ciência de Dados e Machine Learning, CEUB
