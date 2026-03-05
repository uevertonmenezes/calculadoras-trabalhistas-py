from decimal import Decimal


TABELA_INSS_2026 = [
    {
        "limite_superior": Decimal("1621.00"),
        "aliquota": Decimal("0.075"),
        #"parcela_deduzir": Decimal("0.00")
    },

    {
        "limite_superior": Decimal("2902.84"),
        "aliquota": Decimal("0.09"),
        #"parcela_deduzir": Decimal("24.32")
    },

    {
        "limite_superior": Decimal("4354.27"),
        "aliquota": Decimal("0.12"),
        #"parcela_deduzir": Decimal("111.40")
    },

    {
        "limite_superior": Decimal("8475.55"),
        "aliquota": Decimal("0.14"),
        #"parcela_deduzir": Decimal("198.49")
    },
]


TETO_INSS_2026 = Decimal("8475.55")