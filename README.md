# WorldCupCompiler (WCC) 🏆

O **WorldCupCompiler (WCC)** é um front-end de compilador estruturado para uma **Linguagem de Domínio Específico (DSL)** desenvolvida em **Python** utilizando a biblioteca **Lark**. O objetivo principal do projeto é fornecer uma ferramenta declarativa para simular, auditar e gerenciar a fase de grupos da Copa do Mundo da FIFA 2026 de forma fidedigna aos critérios utilizados na vida real.

Este projeto foi desenvolvido pelos estudantes **Gabriel Cortez** e **Rodrigo Campos** como projeto avaliativo para a disciplina de **Compiladores**, ministrada pelo professor **Luis Carlos** da **Escola Politécnica da Universidade de Pernambuco (POLI/UPE)**.

---

## 🚀 Filosofia do Projeto

Alinhado com a premissa prática da disciplina em que foram solicitadas **Originalidade + Utilidade > Complexidade**, o `WorldCupCompiler` abstrai regulamentos esportivos internacionais em uma sintaxe limpa e legível, de forma fidedigna aos critérios utilizados na vida real.

O principal diferencial do projeto é o **Analisador Semântico**, que atua como um "auditor" das regras de sorteio e integridade da FIFA, impedindo inconsistências lógicas antes de computar os resultados.

---

## 📁 Estrutura do Projeto

O repositório segue os padrões de modularidade essenciais para o desenvolvimento de software e compiladores:

```
WCC-DSL-Compiladores/
│
├── main.py                                # Ponto de entrada: pipeline completo do compilador
├── requirements.txt                       # Dependências Python
│
├── src/                                   # Componentes fundamentais do front-end
│   ├── __init__.py
│   ├── grammar.py                         # Fase 1 e 2: regras léxicas e gramática livre de contexto (Lark)
│   ├── semantic.py                        # Fase 3: análise semântica com validação de escopo e contexto
│   └── interpreter.py                    # Fase 4: cálculo de pontuações e geração da classificação final
│
└── exemplos/
    ├── exemplo_inicial.wcc                # ✅ Programa válido com os 12 grupos reais da WCC 2026
    └── erros/
        ├── erro_selecao_duplicada.wcc     # ❌ Seleção declarada duas vezes no mesmo grupo
        ├── erro_pote_duplicado.wcc        # ❌ Dois times no mesmo pote técnico de sorteio
        ├── erro_limite_geografico.wcc     # ❌ Três seleções europeias no mesmo grupo
        ├── erro_selecao_nao_declarada.wcc # ❌ Confronto com seleção não declarada no escopo
        └── erro_excesso_jogos.wcc         # ❌ Seleção disputando mais de 3 jogos
```

---

## 💻 Como Executar

**Pré-requisito:** Python 3.10 ou superior.

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o pipeline completo

Passe um arquivo `.wcc` como argumento. O compilador realizará a análise sintática, as validações semânticas das regras da FIFA (potes e continentes) e exibirá no terminal a classificação calculada de cada grupo, seguida pelo ranking unificado dos melhores terceiros colocados:

```bash
python main.py exemplos/exemplo_inicial.wcc
```

### 3. Testar os cenários de erro semântico

Cada arquivo abaixo força uma violação específica das regras de negócio. Ao executá-los, o compilador emitirá uma mensagem `❌ Erro Semântico [...]` e encerrará a execução sem gerar classificação:

```bash
python main.py exemplos/erros/erro_selecao_duplicada.wcc
python main.py exemplos/erros/erro_pote_duplicado.wcc
python main.py exemplos/erros/erro_limite_geografico.wcc
python main.py exemplos/erros/erro_selecao_nao_declarada.wcc
python main.py exemplos/erros/erro_excesso_jogos.wcc
```

---

## 🗣️ Especificação da Linguagem WCC

A DSL permite descrever grupos de uma copa com suas seleções e confrontos. Um programa WCC é composto por um ou mais blocos `Grupo`.

### Estrutura geral

```
Grupo <ID> {
    Selecao <ID> (pote: <1-4>, continente: <ID>)
    ...
    Confronto <ID> <PLACAR> x <PLACAR> <ID>
    ...
}
```

### Elementos léxicos (Tokens)

| Token      | Expressão Regular | Descrição                                           |
|------------|-------------------|-----------------------------------------------------|
| `ID`       | `[A-Za-zÀ-ÿ_]+`  | Identificador: nome de grupo, seleção ou continente |
| `POTE`     | `[1-4]`           | Número inteiro de 1 a 4 representando o pote técnico|
| `PLACAR`   | `[0-9]+`          | Número inteiro não-negativo representando gols      |
| Comentário | `#[^\n]*`         | Ignorado pelo compilador (início com `#`)           |
| Espaços    | `[ \t\n\r]+`      | Ignorados pelo compilador                           |

### Palavras reservadas

`Grupo`, `Selecao`, `Confronto`, `pote`, `continente`, `x`

### Exemplo de código válido

```wcc
# Declarar um grupo com suas quatro seleções e jogos
Grupo A {
    Selecao Brasil (pote: 1, continente: AmericaDoSul)
    Selecao Marrocos (pote: 2, continente: Africa)
    Selecao Escocia (pote: 3, continente: Europa)
    Selecao Haiti (pote: 4, continente: Na_e_Central_America)

    Confronto Brasil 1 x 1 Marrocos
    Confronto Haiti 0 x 1 Escocia
    Confronto Escocia 0 x 1 Marrocos
    Confronto Brasil 3 x 0 Haiti
}
```

---

## 📐 Gramática Livre de Contexto (EBNF)

```ebnf
start       ::= grupo*

grupo       ::= "Grupo" ID "{" comando* "}"

comando     ::= selecao
              | confronto

selecao     ::= "Selecao" ID "(" "pote" ":" POTE "," "continente" ":" ID ")"

confronto   ::= "Confronto" ID PLACAR "x" PLACAR ID

POTE        ::= /[1-4]/
PLACAR      ::= /[0-9]+/
ID          ::= /[A-Za-zÀ-ÿ_]+/
```

A gramática é **livre de contexto** e implementada com o parser **Lark** usando o algoritmo **Earley** (padrão da biblioteca para gramáticas ambíguas ou com recursão à esquerda).

---

## 🏗️ Arquitetura do Compilador

O pipeline segue as quatro fases clássicas de um front-end de compilador:

```
Arquivo .wcc
     │
     ▼
┌─────────────────────┐
│  FASE 1 + 2         │  grammar.py
│  Análise Léxica e   │  → Tokenização via Lark
│  Sintática          │  → Construção da AST
└────────┬────────────┘
         │  AST (Árvore de Derivação)
         ▼
┌─────────────────────┐
│  FASE 3             │  semantic.py
│  Análise Semântica  │  → Percurso da AST
│                     │  → Validação das regras FIFA
└────────┬────────────┘
         │  AST validada
         ▼
┌─────────────────────┐
│  FASE 4             │  interpreter.py
│  Interpretador      │  → Cálculo de pontos e saldo
│                     │  → Geração das tabelas finais
└────────┬────────────┘
         │
         ▼
    Saída no terminal
    (Classificações + Ranking de Terceiros)
```

### Fase 1 e 2 — Análise Léxica e Sintática (`grammar.py`)

Define a gramática formal da DSL usando a sintaxe EBNF do Lark. O parser é instanciado como `analisador_copa` e expõe o método `.parse(codigo)`, que:
- Tokeniza o código-fonte (análise léxica);
- Constrói a **Árvore Sintática Abstrata (AST)** segundo as regras da gramática (análise sintática);
- Lança `lark.exceptions.UnexpectedToken` ou `lark.exceptions.UnexpectedCharacters` em caso de erro sintático.

### Fase 3 — Análise Semântica (`semantic.py`)

A função `avalie_copa(tree)` percorre a AST recursivamente com **pattern matching** (`match/case`) e submete cada grupo à **Tabela de Símbolos**, mantendo as seguintes estruturas de controle por escopo:

| Estrutura              | Propósito                                           |
|------------------------|-----------------------------------------------------|
| `selecoes_declaradas`  | Conjunto de IDs de seleções já vistas no grupo      |
| `potes_preenchidos`    | Conjunto de inteiros (1–4) de potes já ocupados     |
| `continentes_contagem` | Dicionário contando seleções por confederação       |
| `jogos_por_selecao`    | Dicionário contando partidas disputadas por seleção |

### Fase 4 — Interpretador (`interpreter.py`)

A função `interpretar_copa(tree, memoria_global)` percorre a AST já validada e:
- Inicializa os contadores de pontos, gols pró, gols contra e saldo de gols para cada seleção;
- Aplica a tabela de pontos FIFA (vitória = 3 pts, empate = 1 pt, derrota = 0 pts);
- Ordena o ranking de cada grupo pelos critérios: **pontos → saldo → gols pró**;
- Coleta todos os terceiros colocados e aplica o mesmo critério de ordenação globalmente para determinar os **8 melhores terceiros** que avançam de fase.

---

## 🛑 Validações Semânticas (Regras de Negócio)

Para que um programa WCC compile e gere resultados com sucesso, ele deve ser submetido à Tabela de Símbolos e respeitar as seguintes restrições em tempo de análise:

| # | Regra                           | Descrição                                                                          | Arquivo de Teste                          |
|---|---------------------------------|------------------------------------------------------------------------------------|-------------------------------------------|
| 1 | Seleção Duplicada               | Nenhuma seleção pode ser declarada mais de uma vez no mesmo grupo                  | `erros/erro_selecao_duplicada.wcc`        |
| 2 | Equilíbrio de Potes (Seed System) | Cada grupo deve ter exatamente uma seleção de cada pote técnico (1, 2, 3 e 4)   | `erros/erro_pote_duplicado.wcc`           |
| 3 | Restrição Geográfica (FIFA)     | Máximo de 1 seleção por confederação por grupo, exceto Europa (máximo 2)           | `erros/erro_limite_geografico.wcc`        |
| 4 | Consistência de Identificadores | Seleções em confrontos devem ter sido declaradas previamente no escopo do grupo    | `erros/erro_selecao_nao_declarada.wcc`    |
| 5 | Integridade de Tabela           | Nenhuma equipe pode ultrapassar o limite regulamentar de 3 jogos na fase de grupos | `erros/erro_excesso_jogos.wcc`            |

---

## 🛠️ Tecnologias e Bibliotecas

| Tecnologia       | Uso                                                                   |
|------------------|-----------------------------------------------------------------------|
| **Python 3.10+** | Linguagem de implementação (necessário para `match/case`)             |
| **Lark 1.x**     | Framework de parsing com suporte a EBNF, algoritmos Earley e LALR(1) |
