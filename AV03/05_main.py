"""Demonstração funcional do MVP - AV 03 | Schulz S.A.
Executar: python3 05_main.py
"""
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location("classes_mvp", Path(__file__).with_name("04_classes.py"))
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)
BancoDados = modulo.BancoDados
Tecnico = modulo.Tecnico
Equipamento = modulo.Equipamento
Medicao = modulo.Medicao
ErroValidacao = modulo.ErroValidacao


def executar_demo() -> None:
    caminho_banco = Path(__file__).with_name("schulz_av03_demo.db")
    # O banco é de demonstração: recriado a cada execução para evitar duplicidade nos testes.
    if caminho_banco.exists():
        caminho_banco.unlink()
    banco = BancoDados(caminho_banco)

    print("=" * 68)
    print("MVP SCHULZ S.A. | AV 03 - CADASTRO E CONTROLE DE MEDIÇÕES")
    print("=" * 68)

    # Identificação baseada no arquivo "Registro MMC.xlsx", aba Report.
    # O e-mail não consta na planilha; endereço fictício técnico exigido pelo esquema AV02.
    tecnico = Tecnico("José A. Rosa Jr", "16858-0", "nao-informado@example.invalid", "Dimensional", "TECNICO")
    id_tecnico = tecnico.salvar(banco)

    equipamento = Equipamento(
        "5896", "Dispositivo de controle", "Não se aplica", "Não consta",
        "---", "Dispositivo de controle", None, "703.1208"
    )
    id_equipamento = equipamento.salvar(banco)

    # Dados transcritos de "Registro MMC.xlsx", aba Report, em 13/08/2026.
    # Upper Tol e Lower Tol são desvios em relação ao valor nominal.
    dados_reais = [
        ("PLANICIDADE_REF", 0.0000000, 0.0500000, 0.0000000, 0.0021670, 0.0022670),
        ("ENTRE CENTROS_REF", 0.0000000, 0.0400000, 0.0000000, 0.0274147, 0.0274147),
        ("62P_DIÂMETRO 1", 6.0750000, 0.0100000, -0.0100000, 6.0787295, 6.0787295),
        ("62P_POSIÇÃO 1", 0.0000000, 0.1000000, 0.0000000, 0.4295522, 0.4295522),
        ("62P_DIÂMETRO 2", 6.0750000, 0.0100000, -0.0100000, 6.0781314, 6.0780314),
        ("62P_POSIÇÃO 2", 0.0000000, 0.1000000, 0.0000000, 0.2446114, 0.2446114),
        ("13P_DIÂMETRO 1", 16.9640000, 0.0100000, -0.0100000, 16.9684482, 16.9684482),
        ("13P_POSIÇÃO 1", 0.0000000, 0.1000000, 0.0000000, 0.9590437, 0.9590437),
        ("13P_DIÂMETRO 2", 16.9640000, 0.0100000, -0.0100000, 16.9698259, 16.9698259),
        ("13P_POSIÇÃO 2", 0.0000000, 0.1000000, 0.0000000, 0.2355755, 0.2355755),
        ("106P_DIÂMETRO 1", 6.3450000, 0.0100000, -0.0100000, 6.3463135, 6.3463135),
        ("106P_POSIÇÃO 1", 0.0000000, 0.1000000, 0.0000000, 0.1326897, 0.1316897),
        ("106P_DIÂMETRO 2", 6.3450000, 0.0100000, -0.0100000, 6.3485617, 6.3485617),
        ("106P_POSIÇÃO 2", 0.0000000, 0.1000000, 0.0000000, 0.8677580, 0.8677580),
    ]

    medicoes = []
    for caracteristica, nominal, tol_sup, tol_inf, actual_1, actual_2 in dados_reais:
        for numero_ensaio, valor in enumerate((actual_1, actual_2), start=1):
            medicao = Medicao(
                id_equipamento, id_tecnico, caracteristica, nominal,
                tol_sup, tol_inf, valor, "mm", "2026-08-13",
                f"Registro MMC.xlsx | ensaio {numero_ensaio}"
            )
            medicao.salvar(banco)
            medicoes.append(medicao)

    print("\n[1] CADASTROS REALIZADOS")
    print(f"Técnico: {Tecnico.buscar(banco, id_tecnico)['nome_tecnico']} (ID {id_tecnico})")
    print(f"Equipamento: {Equipamento.buscar(banco, id_equipamento)['descricao']} "
          f"(código {equipamento.codigo_equipamento}, TAG {equipamento.tag})")

    print("\n[2] TESTE DA REGRA DE TOLERÂNCIA")
    print(f"Registros transcritos da planilha: {len(medicoes)}")
    for medicao in medicoes[:8]:
        print(f"{medicao.caracteristica}: {medicao.valor_obtido:.7f} mm -> {medicao.status}")

    print("\n[3] CONSULTA RELACIONAL COM JOIN")
    consulta = banco.consultar("""
        SELECT m.id_medicao, e.codigo_equipamento, e.descricao AS equipamento,
               t.nome_tecnico AS responsavel, m.caracteristica, m.valor_nominal,
               m.valor_obtido, m.tolerancia_inferior, m.tolerancia_superior,
               m.unidade_medida, m.status, m.data_medicao
        FROM medicao m
        INNER JOIN equipamento e ON e.id_equipamento = m.id_equipamento
        INNER JOIN tecnico t ON t.id_tecnico = m.id_tecnico
        ORDER BY m.id_medicao
    """)
    print("ID | Equipamento | Característica | Nominal | Obtido | Status | Responsável")
    print("-" * 100)
    for linha in consulta:
        print(f"{linha['id_medicao']} | {linha['codigo_equipamento']} - {linha['equipamento']} | "
              f"{linha['caracteristica']} | {linha['valor_nominal']:.2f} | {linha['valor_obtido']:.2f} "
              f"{linha['unidade_medida']} | {linha['status']} | {linha['responsavel']}")

    print("\n[4] TESTE DE TRATAMENTO DE ERRO")
    try:
        Tecnico("", "TEC-ERRO", "email-invalido", "Metrologia")
    except ErroValidacao as erro:
        print(f"Validação capturada corretamente: {erro}")

    print("\n[5] RESUMO")
    resumo = banco.consultar("SELECT status, COUNT(*) AS quantidade FROM medicao GROUP BY status ORDER BY status")
    for item in resumo:
        print(f"{item['status']}: {item['quantidade']}")
    print(f"\nBanco de demonstração criado em: {caminho_banco.name}")
    print("Execução concluída.")


if __name__ == "__main__":
    executar_demo()
