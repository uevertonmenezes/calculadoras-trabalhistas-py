def calcular_horas_extras(
        salario_bruto: float,
        hora_mes: float,
        hora_extra50: str,
        hora_extra100: str,
        hora_noturna: str
) -> dict:

    def converter_hora(hora: str) -> int:
        try:
            h, m = map(int, hora.split(':'))
            if h < 0 or h >= 24 or m < 0 or m >= 60:
                raise ValueError
            return h * 60 + m
        except:
            raise ValueError(f"Formato inválido de hora: {hora}. Use HH:MM")

    min_extra50 = converter_hora(hora_extra50)
    min_extra100 = converter_hora(hora_extra100)
    min_noturna = converter_hora(hora_noturna)

    valor_hora = salario_bruto / hora_mes
    valor_minuto = valor_hora / 60

    valor_extra50 = min_extra50 * valor_minuto * 1.5
    valor_extra100 = min_extra100 * valor_minuto * 2
    valor_noturna = (min_noturna * valor_minuto * 1.5) * 1.20

    total = valor_extra50 + valor_extra100 + valor_noturna

    return {
        "valor_hora_trabalhada": round(valor_hora, 2),
        "total_hora_extra50": round(valor_extra50, 2),
        "total_hora_extra100": round(valor_extra100, 2),
        "total_hora_noturna": round(valor_noturna, 2),
        "total_geral": round(total, 2)
    }