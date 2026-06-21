# WorldCupCompiler (WCC) 🏆

O **WorldCupCompiler (WCC)** é um front-end de compilador estruturado para uma Linguagem de Domínio Específico (DSL) desenvolvida em **Python** utilizando a biblioteca **Lark**. O objetivo principal do projeto é fornecer uma ferramenta declarativa para simular, auditar e gerenciar a fase de grupos da Copa do Mundo da FIFA.

Este projeto foi desenvolvido pelos estudantes Gabriel Cortez e Rodrigo Campos como projeto avaliativo para a disciplina de **Compiladores**, ministrada pelo professor **Luis Carlos** da **Escola Politécnica da Universidade de Pernambuco (POLI/UPE)**.

---

## 🚀 Filosofia do Projeto

Alinhado com a premissa prática da disciplina em que foram solicitadas **Originalidade + Utilidade > Complexidade**, o `WorldCupCompiler` abstrai regulamentos esportivos internacionais em uma sintaxe limpa e legível, de forma fidedigna aos critérios utilizados na vida real. 

O principal ponto do projeto é o **Analisador Semântico** que desenvolvemos, que atua como um "auditor" das regras de sorteio e integridade da FIFA, impedindo inconsistências lógicas antes de computar os resultados.

---

## 📁 Estrutura

O repositório segue os padrões de modularidade essenciais para o desenvolvimento de software e compiladores:

* `src/`: Contém os componentes fundamentais do front-end da linguagem.
    * `grammar.py`: Arquivo de definição das regras léxicas (tokens) e gramática livre de contexto (sintática) no Lark.
    * `semantic.py`: Analisador semântico estruturado para a AST (Abstract Syntax Tree) com validação de escopo e contexto.
    * `interpreter.py`: Processa e realiza o cálculo de pontuações padrão FIFA, gerando uma classificação final.
* `exemplos/`: Scripts de teste escrito na extensão própria da DSL para validação de fluxos ideais e tratamento de erros semânticos específicos.
* `main.py`: Ponto de entrada do interpretador responsável pelo pipeline completo de "compilação".

---

## 🛑 Validações Semânticas (Regras de Negócio)

Para que um programa escrito na DSL compile e gere resultados com sucesso, ele deve ser submetido à Tabela de Símbolos e respeitar as seguintes restrições em tempo de execução:

1.  **Regra de Sorteio (Restrição Geográfica):** Impede a presença de mais de uma seleção da mesma confederação continental no mesmo grupo (excetuando a Europa, que aceita até duas pelo regulamento).
2.  **Equilíbrio de Potes (Seed System):** Valida se o grupo possui exatamente uma seleção vinda de cada pote técnico de sorteio (Potes 1, 2, 3 e 4).
3.  **Consistência de Identificadores:** Bloqueia dinamicamente confrontos que utilizem seleções que não foram previamente declaradas dentro do escopo daquele grupo.
4.  **Integridade de Tabela:** Garante por pós-processamento que nenhuma equipe ultrapassará o limite regulamentar de 3 jogos na fase de grupos.

---

## 🛠️ Tecnologias e Bibliotecas

* **Python 3**
* **Lark Parser** (Ferramenta de parsing fundamentada no algoritmo Earley/LALR)

---

## 💻 Como Executar o Compilador

1. Instale a biblioteca necessária via terminal:
```bash
pip install -r requirements.txt
