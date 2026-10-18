-- ==============================================================================
-- UNIDADE CURRICULAR: PROJETO APLICADO I
-- EMPRESA PARCEIRA: SCHULZ S.A.
-- ITEM 03: SCRIPT DDL DE CRIACAO DAS TABELAS (SQLite)
-- Professores: Prof. MSc. Hugo Menezes Barra | Prof. Rodrigo Losina
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- TABELA 1: cadastro centralizado de tecnicos e solicitantes
CREATE TABLE IF NOT EXISTS tecnico (
    id_tecnico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_tecnico TEXT NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    setor TEXT NOT NULL,
    tipo_pessoa TEXT NOT NULL DEFAULT 'TECNICO'
        CHECK (tipo_pessoa IN ('TECNICO', 'SOLICITANTE', 'AMBOS'))
);

-- TABELA 2: cadastro do instrumento/equipamento calibrado
CREATE TABLE IF NOT EXISTS equipamento (
    id_equipamento INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_equipamento TEXT NOT NULL UNIQUE,
    tag TEXT,
    descricao TEXT NOT NULL,
    modelo TEXT,
    fabricante TEXT,
    numero_serie TEXT,
    tipo_instrumento TEXT,
    id_solicitante INTEGER,
    fornecedor TEXT,
    procedimento TEXT,
    data_calibracao TEXT,
    temperatura_ambiente REAL,
    padrao_utilizado TEXT,
    observacoes TEXT,
    FOREIGN KEY (id_solicitante) REFERENCES tecnico(id_tecnico)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- TABELA 3: resultados de medicao relacionados a equipamento e tecnico
CREATE TABLE IF NOT EXISTS medicao (
    id_medicao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_equipamento INTEGER NOT NULL,
    id_tecnico INTEGER NOT NULL,
    plano_medicao TEXT,
    desenho TEXT,
    peca_analisada TEXT,
    caracteristica TEXT NOT NULL,
    parametro TEXT,
    valor_nominal REAL,
    tolerancia_superior REAL,
    tolerancia_inferior REAL,
    valor_obtido REAL,
    valor_obtido_2 REAL,
    media_medicoes REAL,
    desvio_padrao REAL,
    desvio REAL,
    incerteza_medicao REAL,
    unidade_medida TEXT,
    data_medicao TEXT,
    horario_medicao TEXT,
    status TEXT NOT NULL DEFAULT 'PENDENTE'
        CHECK (status IN ('APROVADO', 'REPROVADO', 'PENDENTE', 'NAO_AVALIADO')),
    observacoes TEXT,
    FOREIGN KEY (id_equipamento) REFERENCES equipamento(id_equipamento)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_tecnico) REFERENCES tecnico(id_tecnico)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Regras de negocio para impedir uso de pessoa com papel incorreto.
CREATE TRIGGER IF NOT EXISTS trg_equipamento_solicitante_insert
BEFORE INSERT ON equipamento
WHEN NEW.id_solicitante IS NOT NULL
 AND (SELECT tipo_pessoa FROM tecnico WHERE id_tecnico = NEW.id_solicitante)
     NOT IN ('SOLICITANTE', 'AMBOS')
BEGIN
    SELECT RAISE(ABORT, 'A pessoa associada ao equipamento deve ser SOLICITANTE ou AMBOS');
END;

CREATE TRIGGER IF NOT EXISTS trg_equipamento_solicitante_update
BEFORE UPDATE OF id_solicitante ON equipamento
WHEN NEW.id_solicitante IS NOT NULL
 AND (SELECT tipo_pessoa FROM tecnico WHERE id_tecnico = NEW.id_solicitante)
     NOT IN ('SOLICITANTE', 'AMBOS')
BEGIN
    SELECT RAISE(ABORT, 'A pessoa associada ao equipamento deve ser SOLICITANTE ou AMBOS');
END;

CREATE TRIGGER IF NOT EXISTS trg_medicao_tecnico_insert
BEFORE INSERT ON medicao
WHEN (SELECT tipo_pessoa FROM tecnico WHERE id_tecnico = NEW.id_tecnico)
     NOT IN ('TECNICO', 'AMBOS')
BEGIN
    SELECT RAISE(ABORT, 'A pessoa responsavel pela medicao deve ser TECNICO ou AMBOS');
END;

CREATE TRIGGER IF NOT EXISTS trg_medicao_tecnico_update
BEFORE UPDATE OF id_tecnico ON medicao
WHEN (SELECT tipo_pessoa FROM tecnico WHERE id_tecnico = NEW.id_tecnico)
     NOT IN ('TECNICO', 'AMBOS')
BEGIN
    SELECT RAISE(ABORT, 'A pessoa responsavel pela medicao deve ser TECNICO ou AMBOS');
END;

-- Impede alterar o papel de uma pessoa de forma que invalide vinculos existentes.
CREATE TRIGGER IF NOT EXISTS trg_tecnico_tipo_pessoa_update
BEFORE UPDATE OF tipo_pessoa ON tecnico
WHEN (
    (NEW.tipo_pessoa = 'TECNICO' AND EXISTS (SELECT 1 FROM equipamento e WHERE e.id_solicitante = OLD.id_tecnico))
    OR (NEW.tipo_pessoa = 'SOLICITANTE' AND EXISTS (SELECT 1 FROM medicao m WHERE m.id_tecnico = OLD.id_tecnico))
)
BEGIN
    SELECT RAISE(ABORT, 'O novo papel e incompativel com os relacionamentos existentes');
END;

-- Indices para consultas recorrentes
CREATE INDEX IF NOT EXISTS idx_medicao_equipamento ON medicao(id_equipamento);
CREATE INDEX IF NOT EXISTS idx_medicao_tecnico ON medicao(id_tecnico);
CREATE INDEX IF NOT EXISTS idx_medicao_caracteristica ON medicao(caracteristica);
CREATE INDEX IF NOT EXISTS idx_equipamento_solicitante ON equipamento(id_solicitante);
