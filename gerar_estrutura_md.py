from pathlib import Path

# Gera automaticamente 01_estrutura.md para o projeto Schulz S.A.
conteudo = r'''
# 01_estrutura.md — Estrutura do Banco de Dados

**Unidade Curricular:** Projeto Aplicado I  
**Empresa parceira:** Schulz S.A.  
**Tema 02:** Modelagem e Estruturação de Banco de Dados  
**Professores:** Prof. MSc. Hugo Menezes Barra | Prof. Rodrigo Losina

## 1. Contexto e objetivo

Na Entrega 01, o grupo identificou que o processo de calibração utiliza diferentes planilhas e estruturas para registrar equipamentos, solicitantes, técnicos, resultados de medição, incerteza, padrões, critérios de aceitação e informações usadas na emissão dos certificados. Essa fragmentação pode provocar duplicidade, inconsistências, perda de histórico e dificuldade de rastreabilidade.

O objetivo desta etapa é propor um modelo relacional inicial em SQLite para organizar os dados de equipamentos, técnicos/solicitantes e medições. Este arquivo é gerado automaticamente pelo script `gerar_estrutura_md.py`, conforme o guia prático da Entrega 02.

## 2. Entidades principais

### 2.1. Técnico/Solicitante — tabela `tecnico`

A tabela `tecnico` mantém um cadastro único das pessoas que participam do processo. Os campos `id_tecnico`, `nome_tecnico`, `matricula`, `email` e `setor` identificam e descrevem a pessoa. O campo `tipo_pessoa` informa se ela atua como `TECNICO`, `SOLICITANTE` ou `AMBOS`. Essa abordagem permite que uma pessoa que exerça os dois papéis seja cadastrada uma única vez, evitando registros duplicados. O nome da tabela foi mantido como `tecnico`, conforme o guia de DDL.

### 2.2. Equipamento — tabela `equipamento`

A tabela registra o instrumento ou dispositivo calibrado. Inclui código, TAG, descrição, modelo, fabricante, número de série e tipo de instrumento. Também pode guardar fornecedor, procedimento, data de calibração, temperatura ambiente, padrão utilizado e observações. O campo `id_solicitante` referencia o cadastro da pessoa solicitante em `tecnico`, em vez de repetir o nome como texto livre.

### 2.3. Medição — tabela `medicao`

A tabela armazena os resultados de cada característica avaliada. Inclui plano de medição, desenho, peça analisada, característica, parâmetro, valor nominal, tolerâncias superior e inferior, valor obtido, eventual segundo valor, média, desvio-padrão, desvio, incerteza, unidade, data, horário, status e observações. Cada medição referencia um equipamento e o técnico responsável por meio de chaves estrangeiras. Os campos refletem os dados identificados na Atividade 1, incluindo `Characteristic`, `Actual`, `Nominal`, `Upper Tol`, `Lower Tol` e `Deviation`.

## 3. Relacionamentos entre as entidades

- Uma pessoa com papel de solicitante pode estar relacionada a vários equipamentos: `tecnico` 1:N `equipamento`, por `id_solicitante`.
- Um equipamento pode ter várias medições históricas: `equipamento` 1:N `medicao`, por `id_equipamento`.
- Um técnico pode executar várias medições: `tecnico` 1:N `medicao`, por `id_tecnico`.
- As chaves estrangeiras impedem referências a registros inexistentes quando a integridade referencial está habilitada na conexão SQLite.

O campo `tipo_pessoa` e gatilhos SQL impedem associar como solicitante uma pessoa que não tenha papel `SOLICITANTE` ou `AMBOS`, e impedem associar à medição uma pessoa que não tenha papel `TECNICO` ou `AMBOS`.

## 4. Por que evitar dados duplicados

Armazenar os dados de uma pessoa uma única vez reduz divergências de grafia, e-mail, matrícula e setor. Se os dados fossem digitados novamente em cada equipamento ou medição, uma atualização poderia ocorrer em uma planilha e não em outra. Com o cadastro centralizado, equipamentos e medições apontam para a pessoa por identificadores (`id_solicitante` e `id_tecnico`).

A separação entre equipamento e medição também evita repetir a identificação completa do instrumento em cada resultado. Um equipamento pode acumular muitas medições ao longo do tempo, mantendo o histórico relacionado pelo seu identificador. Essa estrutura melhora a consistência, a rastreabilidade e a manutenção dos dados.

## 5. Tipos e restrições de integridade

- `INTEGER` é usado para identificadores; as chaves primárias usam `PRIMARY KEY AUTOINCREMENT`.
- `TEXT` armazena nomes, códigos, descrições, datas, horários e classificações.
- `REAL` armazena valores numéricos de medição, tolerâncias, incerteza e temperatura.
- A matrícula da pessoa e o código do equipamento são únicos (`UNIQUE`).
- Campos essenciais, como nome, matrícula, e-mail, setor, código do equipamento, descrição e característica medida, são obrigatórios (`NOT NULL`).
- `CHECK` restringe `tipo_pessoa` aos valores `TECNICO`, `SOLICITANTE` e `AMBOS`, e restringe o status da medição a `APROVADO`, `REPROVADO`, `PENDENTE` ou `NAO_AVALIADO`.
- O script SQL ativa a integridade referencial com `PRAGMA foreign_keys = ON;` e define chaves estrangeiras com ações `ON UPDATE CASCADE` e `ON DELETE RESTRICT`.
- Recomenda-se armazenar datas no formato `AAAA-MM-DD` e horários em formato consistente.

## 6. Cuidados com qualidade dos dados

Antes da importação de planilhas, valores como `------`, `00/00/0000` e `#REF!` devem ser tratados como possíveis marcadores de ausência ou erro, não como valores válidos. O valor numérico zero não deve ser convertido automaticamente em dado ausente, pois pode representar uma medição real. Também é necessário validar unidades, separadores decimais, tolerâncias e a correspondência entre as características importadas e o instrumento correto.

## 7. Escopo e limitações desta entrega

Esta entrega apresenta a estrutura relacional, o dicionário de dados e o script DDL executável. Ela não realiza a importação automática de todas as planilhas, não integra diretamente a Máquina de Medição por Coordenadas (MMC)/Calypso, não implementa integralmente os cálculos de incerteza e critérios de aceitação e não gera certificados automaticamente. Padrões, fornecedores, procedimentos e certificados permanecem como atributos textuais nesta versão simplificada e poderão ser normalizados em entidades próprias se o escopo futuro exigir. A estrutura deve ser validada com os responsáveis da Schulz S.A. antes de uso operacional.

'''

caminho_saida = Path(__file__).resolve().with_name("01_estrutura.md")
with open(caminho_saida, "w", encoding="utf-8") as arquivo:
    arquivo.write(conteudo.strip() + "\n")

print(f"Documentação gerada com sucesso: {caminho_saida.name}")
print(f"Total de linhas: {len((conteudo.strip() + chr(10)).splitlines())}")
