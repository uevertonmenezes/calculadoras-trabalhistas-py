from decimal import Decimal


TABELA_IRPF_2026 = [
    {
        "base_ate": Decimal("2428.80"),
        "aliquota": Decimal("0.00"),
        "parcela_deduzir": Decimal("0.00")
    },

    {
        "base_ate": Decimal("2826.65"),
        "aliquota": Decimal("0.075"),
        "parcela_deduzir": Decimal("182.16")
    },

    {
        "base_ate": Decimal("3751.05"),
        "aliquota": Decimal("0.15"),
        "parcela_deduzir": Decimal("394.16")
    },

    {
        "base_ate": Decimal("4664.68"),
        "aliquota": Decimal("0.225"),
        "parcela_deduzir": Decimal("675.49")
    },

    {
        "base_ate": Decimal("Infinity"),
        "aliquota": Decimal("0.275"),
        "parcela_deduzir": Decimal("908.73")
    },
]


DEDUCAO_DEPENDENTE = Decimal("189.59")
ABATIMENTO_ISENCAO_2026 = Decimal("312.89")
LIMITE_ISENCAO_2026 = Decimal("5000.00")