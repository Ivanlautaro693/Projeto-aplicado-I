"""AV 03 - Projeto Aplicado I | Schulz S.A.
Classes de dominio, persistencia SQLite e regras de validacao metrologica.
Compatibilidade com o esquema da AV 02 (tecnico, equipamento, medicao).
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Optional

TIPOS_PESSOA = {"TECNICO", "SOLICITANTE", "AMBOS"}
STATUS_MEDICAO = {"APROVADO", "REPROVADO", "PENDENTE", "NAO_AVALIADO"}


class ErroValidacao(ValueError):
    """Erro lançado quando um dado viola uma regra de negócio."""


class BancoDados:
    """Gerencia conexões e operações SQL no banco SQLite."""
    def __init__(self, caminho: str | Path = "schulz.db") -> None:
        self.caminho = str(caminho)
        self._criar_estrutura()

    def conectar(self) -> sqlite3.Connection:
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

    def _criar_estrutura(self) -> None:
        # Mantém exatamente as tabelas, campos, constraints e triggers da AV 02.
        sql_path = Path(__file__).with_name("03_banco.sql")
        if not sql_path.exists():
            raise FileNotFoundError("O arquivo 03_banco.sql precisa estar na mesma pasta.")
        with self.conectar() as conexao:
            conexao.executescript(sql_path.read_text(encoding="utf-8"))

    def executar(self, sql: str, parametros: tuple = ()) -> int:
        try:
            with self.conectar() as conexao:
                cursor = conexao.execute(sql, parametros)
                return int(cursor.lastrowid or 0)
        except sqlite3.IntegrityError as erro:
            raise ErroValidacao(f"Falha de integridade: {erro}") from erro
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro SQLite: {erro}") from erro

    def consultar(self, sql: str, parametros: tuple = ()) -> list[dict[str, Any]]:
        try:
            with self.conectar() as conexao:
                return [dict(linha) for linha in conexao.execute(sql, parametros).fetchall()]
        except sqlite3.Error as erro:
            raise RuntimeError(f"Erro SQLite na consulta: {erro}") from erro


class Tecnico:
    def __init__(self, nome_tecnico: str, matricula: str, email: str,
                 setor: str, tipo_pessoa: str = "TECNICO", id_tecnico: Optional[int] = None):
        self.id_tecnico = id_tecnico
        self.nome_tecnico = nome_tecnico.strip()
        self.matricula = matricula.strip()
        self.email = email.strip()
        self.setor = setor.strip()
        self.tipo_pessoa = tipo_pessoa.strip().upper()
        self.validar()

    def validar(self) -> None:
        if not all((self.nome_tecnico, self.matricula, self.email, self.setor)):
            raise ErroValidacao("Nome, matrícula, e-mail e setor são obrigatórios.")
        if "@" not in self.email or "." not in self.email.split("@")[-1]:
            raise ErroValidacao("Informe um e-mail em formato válido.")
        if self.tipo_pessoa not in TIPOS_PESSOA:
            raise ErroValidacao(f"tipo_pessoa deve ser um destes valores: {sorted(TIPOS_PESSOA)}")

    def salvar(self, banco: BancoDados) -> int:
        if self.id_tecnico is None:
            self.id_tecnico = banco.executar(
                "INSERT INTO tecnico (nome_tecnico, matricula, email, setor, tipo_pessoa) VALUES (?, ?, ?, ?, ?)",
                (self.nome_tecnico, self.matricula, self.email, self.setor, self.tipo_pessoa))
        else:
            banco.executar("UPDATE tecnico SET nome_tecnico=?, matricula=?, email=?, setor=?, tipo_pessoa=? WHERE id_tecnico=?",
                           (self.nome_tecnico, self.matricula, self.email, self.setor, self.tipo_pessoa, self.id_tecnico))
        return self.id_tecnico

    @staticmethod
    def buscar(banco: BancoDados, id_tecnico: int) -> Optional[dict]:
        resultado = banco.consultar("SELECT * FROM tecnico WHERE id_tecnico=?", (id_tecnico,))
        return resultado[0] if resultado else None

    @staticmethod
    def listar(banco: BancoDados) -> list[dict]:
        return banco.consultar("SELECT * FROM tecnico ORDER BY nome_tecnico")

    @staticmethod
    def excluir(banco: BancoDados, id_tecnico: int) -> None:
        banco.executar("DELETE FROM tecnico WHERE id_tecnico=?", (id_tecnico,))


class Equipamento:
    def __init__(self, codigo_equipamento: str, descricao: str, modelo: str = "",
                 fabricante: str = "", numero_serie: str = "", tipo_instrumento: str = "",
                 id_solicitante: Optional[int] = None, tag: str = "", id_equipamento: Optional[int] = None):
        self.id_equipamento = id_equipamento
        self.codigo_equipamento = codigo_equipamento.strip()
        self.descricao = descricao.strip()
        self.modelo, self.fabricante = modelo.strip(), fabricante.strip()
        self.numero_serie, self.tipo_instrumento = numero_serie.strip(), tipo_instrumento.strip()
        self.id_solicitante, self.tag = id_solicitante, tag.strip()
        self.validar()

    def validar(self) -> None:
        if not self.codigo_equipamento or not self.descricao:
            raise ErroValidacao("Código e descrição do equipamento são obrigatórios.")

    def salvar(self, banco: BancoDados) -> int:
        campos = (self.codigo_equipamento, self.tag, self.descricao, self.modelo, self.fabricante,
                  self.numero_serie, self.tipo_instrumento, self.id_solicitante)
        if self.id_equipamento is None:
            self.id_equipamento = banco.executar(
                "INSERT INTO equipamento (codigo_equipamento, tag, descricao, modelo, fabricante, numero_serie, tipo_instrumento, id_solicitante) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", campos)
        else:
            banco.executar("UPDATE equipamento SET codigo_equipamento=?, tag=?, descricao=?, modelo=?, fabricante=?, numero_serie=?, tipo_instrumento=?, id_solicitante=? WHERE id_equipamento=?",
                           campos + (self.id_equipamento,))
        return self.id_equipamento

    @staticmethod
    def buscar(banco: BancoDados, id_equipamento: int) -> Optional[dict]:
        resultado = banco.consultar("SELECT * FROM equipamento WHERE id_equipamento=?", (id_equipamento,))
        return resultado[0] if resultado else None

    @staticmethod
    def listar(banco: BancoDados) -> list[dict]:
        return banco.consultar("SELECT * FROM equipamento ORDER BY codigo_equipamento")

    @staticmethod
    def excluir(banco: BancoDados, id_equipamento: int) -> None:
        banco.executar("DELETE FROM equipamento WHERE id_equipamento=?", (id_equipamento,))


class Medicao:
    def __init__(self, id_equipamento: int, id_tecnico: int, caracteristica: str,
                 valor_nominal: float, tolerancia_superior: float, tolerancia_inferior: float,
                 valor_obtido: float, unidade_medida: str = "mm", data_medicao: str = "",
                 observacoes: str = "", id_medicao: Optional[int] = None):
        self.id_medicao, self.id_equipamento, self.id_tecnico = id_medicao, id_equipamento, id_tecnico
        self.caracteristica = caracteristica.strip()
        self.valor_nominal = float(valor_nominal)
        self.tolerancia_superior = float(tolerancia_superior)
        self.tolerancia_inferior = float(tolerancia_inferior)
        self.valor_obtido = float(valor_obtido)
        self.unidade_medida, self.data_medicao, self.observacoes = unidade_medida, data_medicao, observacoes
        self.status = self.validar_tolerancia()

    def validar_tolerancia(self) -> str:
        if not self.caracteristica:
            raise ErroValidacao("A característica medida é obrigatória.")
        if self.tolerancia_inferior > self.tolerancia_superior:
            raise ErroValidacao("A tolerância inferior não pode ser maior que a superior.")
        # Premissa adotada: tolerâncias são desvios em relação ao valor nominal.
        limite_inferior = self.valor_nominal + self.tolerancia_inferior
        limite_superior = self.valor_nominal + self.tolerancia_superior
        return "APROVADO" if limite_inferior <= self.valor_obtido <= limite_superior else "REPROVADO"

    def salvar(self, banco: BancoDados) -> int:
        campos = (self.id_equipamento, self.id_tecnico, self.caracteristica, self.valor_nominal,
                  self.tolerancia_superior, self.tolerancia_inferior, self.valor_obtido,
                  self.status, self.unidade_medida, self.data_medicao, self.observacoes)
        if self.id_medicao is None:
            self.id_medicao = banco.executar(
                "INSERT INTO medicao (id_equipamento, id_tecnico, caracteristica, valor_nominal, tolerancia_superior, tolerancia_inferior, valor_obtido, status, unidade_medida, data_medicao, observacoes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", campos)
        else:
            banco.executar("UPDATE medicao SET id_equipamento=?, id_tecnico=?, caracteristica=?, valor_nominal=?, tolerancia_superior=?, tolerancia_inferior=?, valor_obtido=?, status=?, unidade_medida=?, data_medicao=?, observacoes=? WHERE id_medicao=?",
                           campos + (self.id_medicao,))
        return self.id_medicao

    @staticmethod
    def buscar(banco: BancoDados, id_medicao: int) -> Optional[dict]:
        resultado = banco.consultar("SELECT * FROM medicao WHERE id_medicao=?", (id_medicao,))
        return resultado[0] if resultado else None

    @staticmethod
    def listar(banco: BancoDados) -> list[dict]:
        return banco.consultar("SELECT * FROM medicao ORDER BY id_medicao")

    @staticmethod
    def excluir(banco: BancoDados, id_medicao: int) -> None:
        banco.executar("DELETE FROM medicao WHERE id_medicao=?", (id_medicao,))
