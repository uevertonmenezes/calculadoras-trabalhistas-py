from aliquotas.inss_2026 import TABELA_INSS_2026


def calcular_inss(base: float) -> float:
    if base <= 0:
        return 0.0

    for faixa in TABELA_INSS_2026:
        if base <= faixa["salario_ate"]:
            return (base * faixa["aliquota"]) - faixa["parcela_deduzir"]

    ultima_faixa = TABELA_INSS_2026[-1]
    teto = ultima_faixa["salario_ate"]
    return (teto * ultima_faixa["aliquota"]) - ultima_faixa["parcela_deduzir"]
