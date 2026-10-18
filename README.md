# Projeto Aplicado I — Entrega 02 | Schulz S.A.

**Tema:** Modelagem e Estruturação de Banco de Dados (SQLite)


## Repositório no GitHub

https://github.com/Ivanlautaro693/Projeto-aplicado-I

## Conteúdo do pacote

- `gerar_estrutura_md.py`: gera `01_estrutura.md` automaticamente usando `with open()`, modo `w`, `encoding="utf-8"` e `arquivo.write()`.
- `01_estrutura.md`: explica as três entidades, os relacionamentos e a importância de evitar dados duplicados.
- `gerar_dicionario_md.py`: gera `02_dicionario.md` automaticamente.
- `02_dicionario.md`: mapeia os campos, tipos, obrigatoriedade, restrições e regras de negócio.
- `03_banco.sql`: cria as três tabelas principais `tecnico`, `equipamento` e `medicao`, além de índices e gatilhos de validação.
- `04_entrega_02.pdf`: resumo explicativo do projeto e dos testes realizados.

## Como gerar os Markdown

Abra um terminal na pasta do projeto e execute:

```bash
python3 gerar_estrutura_md.py
python3 gerar_dicionario_md.py
```

Os scripts criam ou sobrescrevem os respectivos arquivos Markdown na mesma pasta.

## Como criar o banco de dados

Com SQLite instalado, execute:

```bash
sqlite3 schulz.db < 03_banco.sql
```

Para listar as tabelas:

```bash
sqlite3 schulz.db ".tables"
```

`PRAGMA foreign_keys = ON;` é aplicado pelo arquivo SQL durante sua execução. Em aplicações que abrem novas conexões SQLite, essa opção deve ser habilitada em cada conexão.

## Modelo e regras

- `tecnico`: cadastro de pessoas com papel `TECNICO`, `SOLICITANTE` ou `AMBOS`.
- `equipamento`: dados do instrumento e referência opcional ao solicitante por `id_solicitante`.
- `medicao`: resultado de medição associado a um equipamento e ao técnico responsável.
- As três tabelas possuem chave primária. Chaves estrangeiras garantem a referência entre os registros.
- Gatilhos impedem o uso de uma pessoa com papel incompatível com o relacionamento.

## Testes efetuados

O script SQL foi executado em uma base SQLite temporária. Foram testadas a criação das três tabelas, inserções válidas, chaves estrangeiras, papéis de técnico/solicitante e rejeição de referências ou papéis inválidos.

## Limites do escopo

Esta entrega não importa automaticamente todas as planilhas, não integra diretamente a MMC/Calypso, não implementa todos os cálculos de incerteza e critérios de aceitação e não emite certificados automaticamente. Esses itens dependem de etapas posteriores e de validação com os responsáveis pelo processo.
