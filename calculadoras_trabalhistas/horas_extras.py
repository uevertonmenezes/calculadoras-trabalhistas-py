from decimal import Decimal, ROUND_HALF_UP


def calcular_horas_extras(
        salario_bruto: float,
        hora_mes: float,
        hora_extra50: str,
        hora_extra100: str,
        hora_extra_noturna: str
) -> dict:

    if hora_mes <= 0:
        raise ValueError("hora_mes deve ser maior que zero.")


    ADICIONAL_50 = Decimal("1.5")
    ADICIONAL_100 = Decimal("2.0")
    ADICIONAL_NOTURNO = Decimal("1.2")


    def converter_hora(hora: str) -> int:
        try:
            h, m = map(int, hora.split(':'))
            if h < 0 or m < 0 or m >= 60:
                raise ValueError
            return h * 60 + m
        except ValueError:
            raise ValueError(f"Formato inválido de hora: {hora}. Use HH:MM")

    salario_bruto = Decimal(str(salario_bruto))
    hora_mes = Decimal(str(hora_mes))

    min_extra50 = Decimal(converter_hora(hora_extra50))
    min_extra100 = Decimal(converter_hora(hora_extra100))
    min_extra_noturna = Decimal(converter_hora(hora_extra_noturna))

    valor_hora = salario_bruto / hora_mes
    valor_minuto = valor_hora / Decimal("60")

    valor_extra50 = min_extra50 * valor_minuto * ADICIONAL_50
    valor_extra100 = min_extra100 * valor_minuto * ADICIONAL_100
    valor_extra_noturna = (min_extra_noturna * valor_minuto * ADICIONAL_NOTURNO) * ADICIONAL_50

    total = valor_extra50 + valor_extra100 + valor_extra_noturna

    def arredondar(valor: Decimal) -> Decimal:
        return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return {
        "valor_hora_trabalhada": float(arredondar(valor_hora)),
        "total_hora_extra50": float(arredondar(valor_extra50)),
        "total_hora_extra100": float(arredondar(valor_extra100)),
        "total_hora_noturna": float(arredondar(valor_extra_noturna)),
        "total_geral": float(arredondar(total)),
    }