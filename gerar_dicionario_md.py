from pathlib import Path

# Gera automaticamente 02_dicionario.md a partir da especificacao de campos abaixo.
# Manter este dicionario sincronizado com 03_banco.sql.
TABELAS = {
    "tecnico": {
        "titulo": "Técnico / Solicitante",
        "campos": [
            ("id_tecnico", "INTEGER", "Sim", "PRIMARY KEY AUTOINCREMENT", "Identificador único da pessoa cadastrada."),
            ("nome_tecnico", "TEXT", "Sim", "NOT NULL", "Nome completo da pessoa."),
            ("matricula", "TEXT", "Sim", "UNIQUE, NOT NULL", "Matrícula ou identificador institucional único."),
            ("email", "TEXT", "Sim", "NOT NULL", "E-mail de contato."),
            ("setor", "TEXT", "Sim", "NOT NULL", "Setor ou área de atuação."),
            ("tipo_pessoa", "TEXT", "Sim", "NOT NULL, DEFAULT 'TECNICO', CHECK", "Papel permitido: TECNICO, SOLICITANTE ou AMBOS."),
        ],
    },
    "equipamento": {
        "titulo": "Equipamento",
        "campos": [
            ("id_equipamento", "INTEGER", "Sim", "PRIMARY KEY AUTOINCREMENT", "Identificador interno do equipamento."),
            ("codigo_equipamento", "TEXT", "Sim", "UNIQUE, NOT NULL", "Código único do instrumento ou dispositivo."),
            ("tag", "TEXT", "Não", "—", "TAG de identificação, quando utilizada."),
            ("descricao", "TEXT", "Sim", "NOT NULL", "Descrição do equipamento."),
            ("modelo", "TEXT", "Não", "—", "Modelo do instrumento."),
            ("fabricante", "TEXT", "Não", "—", "Fabricante do equipamento."),
            ("numero_serie", "TEXT", "Não", "—", "Número de série do instrumento."),
            ("tipo_instrumento", "TEXT", "Não", "—", "Tipo do instrumento ou dispositivo."),
            ("id_solicitante", "INTEGER", "Não", "FK → tecnico.id_tecnico", "Identificador da pessoa solicitante cadastrada; pode ficar vazio se não informado."),
            ("fornecedor", "TEXT", "Não", "—", "Fornecedor associado ao registro."),
            ("procedimento", "TEXT", "Não", "—", "Procedimento utilizado na calibração."),
            ("data_calibracao", "TEXT", "Não", "—", "Data da calibração, preferencialmente AAAA-MM-DD."),
            ("temperatura_ambiente", "REAL", "Não", "—", "Temperatura ambiente registrada."),
            ("padrao_utilizado", "TEXT", "Não", "—", "Identificação textual do padrão utilizado."),
            ("observacoes", "TEXT", "Não", "—", "Observações complementares."),
        ],
    },
    "medicao": {
        "titulo": "Medição",
        "campos": [
            ("id_medicao", "INTEGER", "Sim", "PRIMARY KEY AUTOINCREMENT", "Identificador único da medição."),
            ("id_equipamento", "INTEGER", "Sim", "FK → equipamento.id_equipamento, NOT NULL", "Equipamento relacionado à medição."),
            ("id_tecnico", "INTEGER", "Sim", "FK → tecnico.id_tecnico, NOT NULL", "Técnico responsável pela medição."),
            ("plano_medicao", "TEXT", "Não", "—", "Identificação do plano de medição."),
            ("desenho", "TEXT", "Não", "—", "Identificação do desenho relacionado."),
            ("peca_analisada", "TEXT", "Não", "—", "Peça ou item analisado."),
            ("caracteristica", "TEXT", "Sim", "NOT NULL", "Característica avaliada; corresponde ao campo Characteristic da origem."),
            ("parametro", "TEXT", "Não", "—", "Parâmetro complementar da característica."),
            ("valor_nominal", "REAL", "Não", "—", "Valor nominal; corresponde ao campo Nominal."),
            ("tolerancia_superior", "REAL", "Não", "—", "Tolerância superior; corresponde ao campo Upper Tol."),
            ("tolerancia_inferior", "REAL", "Não", "—", "Tolerância inferior; corresponde ao campo Lower Tol."),
            ("valor_obtido", "REAL", "Não", "—", "Valor obtido; corresponde ao campo Actual."),
            ("valor_obtido_2", "REAL", "Não", "—", "Segundo valor obtido, quando houver."),
            ("media_medicoes", "REAL", "Não", "—", "Média das medições, quando calculada."),
            ("desvio_padrao", "REAL", "Não", "—", "Desvio-padrão, quando calculado."),
            ("desvio", "REAL", "Não", "—", "Desvio em relação ao nominal; corresponde ao campo Deviation."),
            ("incerteza_medicao", "REAL", "Não", "—", "Incerteza associada à medição, se disponível."),
            ("unidade_medida", "TEXT", "Não", "—", "Unidade usada para expressar a medição."),
            ("data_medicao", "TEXT", "Não", "—", "Data da medição, preferencialmente AAAA-MM-DD."),
            ("horario_medicao", "TEXT", "Não", "—", "Horário da medição em formato consistente."),
            ("status", "TEXT", "Sim", "NOT NULL, DEFAULT 'PENDENTE', CHECK", "Status permitido: APROVADO, REPROVADO, PENDENTE ou NAO_AVALIADO."),
            ("observacoes", "TEXT", "Não", "—", "Observações adicionais."),
        ],
    },
}

linhas = [
    "# 02_dicionario.md — Dicionário de Dados do Sistema", "",
    "**Unidade Curricular:** Projeto Aplicado I  ",
    "**Empresa parceira:** Schulz S.A.  ",
    "**Tema 02:** Modelagem e Implementação de Banco de Dados (SQLite)  ",
    "**Professores:** Prof. MSc. Hugo Menezes Barra | Prof. Rodrigo Losina", "",
    "Este documento é gerado automaticamente por `gerar_dicionario_md.py`. Ele descreve os campos das três tabelas definidas em `03_banco.sql`; os tipos e restrições devem permanecer alinhados ao script DDL.", "",
    "## 1. Mapeamento das tabelas e campos", "",
]
for numero, (nome_tabela, info) in enumerate(TABELAS.items(), start=1):
    linhas.extend([f"### 1.{numero}. Tabela: `{nome_tabela}` — {info['titulo']}", "",
        "| Nome do campo | Tipo (SQLite) | Obrigatório | Restrições / chaves | Descrição / regra de negócio |",
        "|---|---|---|---|---|"])
    for campo, tipo, obrigatorio, restricoes, descricao in info["campos"]:
        descricao = descricao.replace("|", "\\|")
        linhas.append(f"| `{campo}` | {tipo} | {obrigatorio} | {restricoes} | {descricao} |")
    linhas.append("")
linhas.extend([
    "## 2. Tipos de dados", "",
    "- `INTEGER`: identificadores inteiros e chaves primárias com incremento automático.",
    "- `TEXT`: nomes, matrículas, códigos, descrições, datas, horários, unidades e classificações.",
    "- `REAL`: valores de medição, nominal, tolerâncias, desvio, incerteza e temperatura.", "",
    "## 3. Regras de integridade", "",
    "A matrícula e o código do equipamento são únicos. Os campos definidos como obrigatórios usam `NOT NULL`. A coluna `tipo_pessoa` aceita apenas `TECNICO`, `SOLICITANTE` ou `AMBOS`; o status aceita `APROVADO`, `REPROVADO`, `PENDENTE` ou `NAO_AVALIADO`. As chaves estrangeiras conectam equipamentos a solicitantes e medições a equipamentos e técnicos. Gatilhos SQL validam a compatibilidade dos papéis das pessoas com esses relacionamentos.", "",
    "## 4. Correspondência com os dados de origem", "",
    "Os campos `caracteristica`, `valor_obtido`, `valor_nominal`, `tolerancia_superior`, `tolerancia_inferior` e `desvio` representam, respectivamente, `Characteristic`, `Actual`, `Nominal`, `Upper Tol`, `Lower Tol` e `Deviation` identificados na planilha de resultados do Calypso Measuring Result descrita na Atividade 1. Campos adicionais cobrem identificação do instrumento, responsável, data, horário, incerteza e demais informações disponíveis no processo. Campos opcionais podem permanecer nulos quando a origem não contém informação; marcadores como `#REF!` e `00/00/0000` devem ser tratados antes da importação.", "",
    "## 5. Observações", "",
    "O dicionário documenta a proposta simplificada desta entrega. Padrões, fornecedores, procedimentos, critérios de aceitação e certificados não foram modelados como tabelas próprias nesta etapa. A implementação operacional deve ser validada com a equipe responsável da Schulz S.A."
])

conteudo = "\n".join(linhas) + "\n"
caminho_saida = Path(__file__).resolve().with_name("02_dicionario.md")
with open(caminho_saida, "w", encoding="utf-8") as arquivo:
    arquivo.write(conteudo)
print(f"Dicionário gerado com sucesso: {caminho_saida.name}")
print(f"Total de linhas: {len(linhas)}; campos mapeados: {sum(len(t['campos']) for t in TABELAS.values())}")
