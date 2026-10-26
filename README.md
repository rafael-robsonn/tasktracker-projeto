# TaskTracker

Sistema de gerenciamento de tarefas via linha de comando, escrito em Python. Projeto cumulativo do Bootcamp II (CEUB). A Fase 2 implementou em Python a lógica planejada na Fase 1 e a Fase 3 empacota a aplicação com Docker.

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
├── Dockerfile                   # Receita da imagem da aplicação
├── docker-compose.yml           # Execução interativa da CLI via Compose
├── requirements.txt             # Dependências do projeto (nenhuma nesta fase)
├── docs/
│   └── planejamento_logico.pdf  # Planejamento lógico da Fase 1
├── data/
│   └── tarefas.json             # Base de dados local, gerada em tempo de execução
└── src/
    └── main.py                  # Código-fonte da aplicação
```

## Como executar

Duas formas: direto com Python ou dentro de um container Docker.

### Com Python local

Requer Python 3.8 ou superior. Nenhuma dependência externa.

```bash
git clone <url-do-repositorio>
cd tasktracker-projeto
python src/main.py
```

(Em Linux e macOS, use `python3` no lugar de `python`.)

### Com Docker

Requer Docker instalado e em execução. Todos os comandos rodam na raiz do repositório.

Como construir a imagem:

```bash
docker build -t tasktracker-app .
```

Como rodar o container em modo isolado:

```bash
docker run -it --rm tasktracker-app
```

Como rodar via orquestração (recomendado):

```bash
docker compose run --rm tasktracker-app
```

O `-it` (e, no Compose, `stdin_open` e `tty`) mantém o terminal interativo, que a aplicação precisa para ler as respostas do menu. O Compose também monta a pasta `data/` do projeto dentro do container, então as tarefas continuam salvas depois que o container é encerrado. No `docker run` simples, os dados ficam só dentro do container e somem quando ele sai; para guardá-los, acrescente `-v ./data:/app/data` (no PowerShell: `-v ${PWD}/data:/app/data`).

## Decisões do Docker

- Imagem base `python:3.11-slim`: Python oficial, sem pacotes extras, imagem pequena.
- `WORKDIR /app` e `COPY src/ /app/src/`: só o código-fonte entra na imagem.
- `ENV PYTHONUNBUFFERED=1`: as mensagens do programa aparecem na hora no terminal, sem buffer.
- `CMD ["python", "src/main.py"]`: o container sobe direto no menu do TaskTracker.

## Regras de negócio implementadas

| Regra | Descrição |
|---|---|
| R1 | Título obrigatório; vazio ou só espaços é recusado. |
| R2 | Prioridade restrita a Alta, Média ou Baixa. |
| R3 | Data limite precisa existir no calendário e não pode ser anterior a hoje. |
| R4 | ID numérico único, nunca reaproveitado após exclusão. |
| R5 | Toda tarefa nasce Pendente; única transição é para Concluída. |
| R6 | Concluir não remove a tarefa, ela fica registrada para histórico. |
| R7 | Exclusão exige confirmação explícita do usuário. |
| R8 | Toda alteração é gravada em disco antes de voltar ao menu. |
| R9 | Entrada inválida nunca derruba o programa. |

## Autor

Rafael Robson Nunes de Araújo, Ciência de Dados e Machine Learning, CEUB
