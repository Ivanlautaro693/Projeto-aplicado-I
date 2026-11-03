# 06_mvp_parte1.md — Documentação Técnica do MVP (Parte 1)

**Unidade Curricular:** Projeto Aplicado I  
**Empresa parceira:** Schulz S.A.  
**Tema:** AV 03 — Construção do MVP (Parte 1)  
**Linguagem:** Python 3  
**Banco de dados:** SQLite  
**Repositório:** https://github.com/Ivanlautaro693/Projeto-aplicado-I

## 1. Objetivo

Esta etapa transforma a modelagem relacional da AV 02 em uma demonstração executável. O MVP permite cadastrar técnicos/solicitantes e equipamentos, registrar medições, avaliar o resultado em relação à tolerância informada e consultar os dados relacionados por meio de `JOIN`.

A implementação reutiliza o esquema da AV 02, preservando as tabelas `tecnico`, `equipamento` e `medicao`, suas colunas, chaves estrangeiras, restrições, índices e gatilhos definidos em `03_banco.sql`.

## 2. Organização e responsabilidades

- `Tecnico`: representa a pessoa cadastrada e valida nome, matrícula, e-mail, setor e papel. Implementa operações de inserir, atualizar, consultar, listar e excluir.
- `Equipamento`: representa o instrumento de medição. Valida os campos obrigatórios e implementa operações CRUD.
- `Medicao`: representa um resultado de medição. Aplica a regra de tolerância e persiste o status calculado. Implementa operações CRUD.
- `BancoDados`: centraliza a abertura de conexões SQLite, habilita `PRAGMA foreign_keys = ON`, executa comandos e converte erros de integridade em mensagens compreensíveis.
- `05_main.py`: instancia os objetos e executa o cenário de demonstração.

## 3. Conceitos de POO aplicados

**Abstração:** cada classe representa um elemento do domínio (pessoa, equipamento ou medição), expondo métodos relacionados à sua responsabilidade.

**Encapsulamento:** os dados e as regras de validação ficam organizados dentro das classes. A persistência é acessada por métodos como `salvar`, `buscar`, `listar` e `excluir`, evitando espalhar comandos SQL pelo script principal.

**Separação de responsabilidades:** `05_main.py` coordena o cenário; as classes de domínio validam e representam os dados; `BancoDados` concentra a comunicação com SQLite.

**Reutilização:** os métodos de persistência são reaproveitados nos diferentes cenários e as consultas recebem parâmetros separados, evitando concatenar valores diretamente no SQL.

## 4. Diagrama textual de classes (UML simplificado)

```text
+---------------------------+
|         BancoDados        |
+---------------------------+
| - caminho: str            |
+---------------------------+
| + conectar()              |
| + executar(sql, params)   |
| + consultar(sql, params)  |
+---------------------------+
             ^
             | utiliza
  +----------+-----------+
  |          |           |
  v          v           v
Tecnico  Equipamento   Medicao
- id      - id          - id
- nome    - codigo      - id_equipamento
- matric. - descricao   - id_tecnico
- email   - fabricante  - caracteristica
- setor   - solicitante - nominal/tolerâncias
- tipo                  - valor_obtido/status
  |          |           |
  +----------+-----------+
       persistem no SQLite

Relacionamentos do banco:
tecnico (1) ---- (N) equipamento, pelo id_solicitante
tecnico (1) ---- (N) medicao, pelo id_tecnico
equipamento (1) - (N) medicao, pelo id_equipamento
```

## 5. Regra de validação metrológica e origem dos dados

A regra foi conferida com a planilha fornecida `Registro MMC.xlsx`, aba `Report`, que apresenta as colunas `Actual`, `Nominal`, `Upper Tol`, `Lower Tol` e `Deviation`. Os valores de `Upper Tol` e `Lower Tol` são desvios em relação ao nominal; portanto:

- Limite inferior = nominal + `Lower Tol`.
- Limite superior = nominal + `Upper Tol`.
- O resultado é `APROVADO` quando o valor medido está dentro dos limites, inclusive.
- Fora do intervalo, o MVP classifica como `REPROVADO`.

Os dados de demonstração foram transcritos do relatório `Registro MMC.xlsx`, referente a 13/08/2026, equipamento de TAG `703.1208` e código `5896`. Foram preservadas as duas leituras (`Actual`) por característica como registros individuais, totalizando 28 medições. Os valores nominais e tolerâncias também foram transcritos da planilha.

Exemplo de dimensão: `62P_DIÂMETRO 1`, nominal 6,075 mm, tolerância superior +0,010 mm e inferior -0,010 mm. A faixa calculada é de 6,065 mm a 6,085 mm; leitura 6,0787295 mm fica dentro da faixa.

Exemplo de posição: `62P_POSIÇÃO 1`, nominal 0, tolerância superior +0,100 mm e inferior 0 mm. A leitura registrada de 0,4295522 mm fica fora da faixa calculada e, pela regra implementada, é classificada como `REPROVADO`. Essa classificação é o resultado matemático do critério informado na planilha; não substitui a avaliação metrológica formal nem interpreta eventuais regras específicas adicionais do procedimento.

**Limite da fonte:** o e-mail do técnico não consta no relatório. Para atender ao campo obrigatório do esquema da AV 02, o programa usa `nao-informado@example.invalid`, endereço fictício de preenchimento técnico, não dado real da Schulz.

## 6. Persistência e tratamento de erros SQL

A aplicação usa o módulo padrão `sqlite3`. Cada conexão habilita as chaves estrangeiras com `PRAGMA foreign_keys = ON`. Os comandos de escrita são executados com parâmetros (`?`) para separar os dados do texto SQL.

São tratados:

- `sqlite3.IntegrityError`: violações de chave única, chave estrangeira, `NOT NULL`, `CHECK` e gatilhos.
- `sqlite3.Error`: demais falhas de execução e consulta.
- `ErroValidacao`: dados inválidos identificados pelas regras da aplicação.

As regras já existentes no banco também são mantidas, incluindo a compatibilidade entre o papel da pessoa (`TECNICO`, `SOLICITANTE` ou `AMBOS`) e os relacionamentos.

## 7. Testes funcionais executados

Execução realizada com `python3 05_main.py`, em banco de demonstração recriado a cada execução (`schulz_av03_demo.db`).

| Teste | Resultado |
|---|---|
| Cadastro do técnico e equipamento identificados no relatório | Sucesso |
| Persistência das duas leituras por característica | 28 medições gravadas |
| Aplicação dos limites calculados a partir do nominal e tolerâncias | Executada |
| Consulta relacional com `JOIN` entre as três tabelas | Sucesso |
| Validação de dados obrigatórios/e-mail | Entrada inválida rejeitada |
| Integridade referencial | Mantida pelo esquema e gatilhos da AV 02 |

Os resultados de aprovação/reprovação são calculados pelo código para cada leitura individual, usando os valores da planilha fornecida. O status calculado pelo MVP deve ser entendido como demonstração da regra implementada, não como substituto do certificado ou da decisão formal do laboratório.

## 8. Como executar

Mantenha na mesma pasta os arquivos `04_classes.py`, `05_main.py` e `03_banco.sql`. Com Python 3 instalado, execute:

```bash
python3 05_main.py
```

Não é necessário instalar bibliotecas externas: `sqlite3`, `pathlib` e `importlib` fazem parte da biblioteca padrão do Python. O script cria o arquivo `schulz_av03_demo.db` na pasta do projeto.

## 9. Limites do MVP

Esta é uma demonstração acadêmica que utiliza valores transcritos de arquivos fornecidos para a atividade. Ela não se conecta ao sistema Calypso/MCC, não importa planilhas automaticamente, não calcula incerteza metrológica e não substitui a aprovação técnica da equipe responsável. Os dados de identificação pessoal foram limitados ao que é necessário para a demonstração; o e-mail é fictício porque não consta da fonte.

## 10. Conclusão

A AV 03 apresenta uma primeira versão executável do MVP, aplicando POO, persistência SQLite, validação de regras de negócio e consulta relacional. A solução mantém continuidade com a estrutura de dados desenvolvida na AV 02 e fornece uma base organizada para evoluções posteriores.
