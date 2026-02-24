from typing import List, Tuple


def converter_hora_para_minutos(hora: str) -> int:
    if len(hora) != 5 or hora[2] != ":":
        raise ValueError(f"Formato inválido: {hora}. Use HH:MM com dois dígitos cada.")

    h_str, m_str = hora.split(":")

    if not (h_str.isdigit() and m_str.isdigit()):
        raise ValueError(f"Formato inválido: {hora}. Use apenas números em HH e MM.")

    h, m = int(h_str), int(m_str)

    if not (0 <= h <= 23):
        raise ValueError(f"Hora inválida: {h:02d}")
    if not (0 <= m <= 59):
        raise ValueError(f"Minuto inválido: {m:02d}")

    return h * 60 + m


def calcular_duracao_intervalo(horario_inicial: str, horario_final: str) -> int:
    inicio = converter_hora_para_minutos(horario_inicial)
    final = converter_hora_para_minutos(horario_final)

    if final < inicio:
        final += 24 * 60

    return final - inicio


def formatar_minutos_hhmm(total_minutos: int) -> str:
    horas = total_minutos // 60
    minutos = total_minutos % 60
    return f"{horas:02d}:{minutos:02d}"


def calcular_total_intervalo(intervalos: List[Tuple[str, str]]) -> str:
    total_minutos = sum(calcular_duracao_intervalo(inicio, fim) for inicio, fim in intervalos)
    return formatar_minutos_hhmm(total_minutos)