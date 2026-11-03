# Projeto Aplicado I — Schulz S.A. | AV 02 + AV 03

**Repositório GitHub:** https://github.com/Ivanlautaro693/Projeto-aplicado-I

Este pacote reúne a modelagem desenvolvida na AV 02 e a primeira implementação do MVP solicitada na AV 03. A organização em pastas evidencia a continuidade entre as etapas.

## AV 02 — Modelagem SQLite
Consulte a pasta `AV02/`, que contém a estrutura, o dicionário de dados, o script SQL, o PDF da entrega anterior e os scripts geradores.

## AV 03 — Construção do MVP (Parte 1)
Consulte a pasta `AV03/`:
- `04_classes.py`: classes `Tecnico`, `Equipamento`, `Medicao` e `BancoDados`, validações, persistência e CRUD.
- `05_main.py`: demonstração de cadastros, medições aprovadas/reprovadas, consulta JOIN e relatório no terminal.
- `03_banco.sql`: esquema compatível com a AV 02, necessário para criar o banco de demonstração.
- `06_mvp_parte1.md` e `07_mvp_parte1.pdf`: documentação técnica.

## Como executar
Abra um terminal dentro da pasta `AV03` e execute:

```bash
python3 05_main.py
```

Requisito: Python 3.9 ou superior. Não são necessárias bibliotecas externas.

O script recria `schulz_av03_demo.db` a cada execução. A demonstração usa 28 leituras transcritas de `Registro MMC.xlsx` (aba Report, 13/08/2026), incluindo nominal, tolerâncias e duas leituras por característica. O e-mail do técnico não consta da fonte e foi substituído por endereço reservado fictício `example.invalid`. Os status são calculados pela regra descrita na documentação e não substituem avaliação metrológica formal.

## Fonte dos dados metrológicos
A interpretação de `Upper Tol` e `Lower Tol` como desvios relativos ao nominal foi conferida no arquivo `Registro MMC.xlsx`, aba `Report`, que apresenta essas colunas ao lado de `Actual` e `Nominal`. A implementação calcula os limites como nominal + tolerância. A classificação resultante é demonstrativa e não substitui certificado ou decisão formal do laboratório.
