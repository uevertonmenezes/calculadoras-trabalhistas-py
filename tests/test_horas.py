import pytest

from calculadoras_trabalhistas.horas import calcular_total


# HORÁRIOS PADRÃO #

INTERVALO_UM = [("07:00", "11:05")]
INTERVALO_DOIS = [("07:00", "11:05"), ("13:00", "17:05")]
INTERVALO_TRES = INTERVALO_DOIS + [("18:00", "20:00")]
INTERVALO_QUATRO = INTERVALO_TRES + [("22:00", "23:00")]
INTERVALO_VARIOS = [
    ("08:00", "09:00"),
    ("09:30", "10:30"),
    ("11:00", "12:00"),
    ("13:00", "14:00"),
    ("15:00", "16:00"),
]


# CASOS BÁSICOS #

@pytest.mark.parametrize(
    "intervalos, esperado",
    [
        (INTERVALO_UM, "04:05"),
        (INTERVALO_DOIS, "08:10"),
        (INTERVALO_TRES, "10:10"),
        (INTERVALO_QUATRO, "11:10"),
        (INTERVALO_VARIOS, "05:00"),
    ]
)
def test_calcular_total_deve_retornar_valor_correto(intervalos, esperado):
    assert calcular_total(intervalos) == esperado


# VALIDAÇÃO DE HORÁRIOS #

def test_horario_final_menor_deve_gerar_erro():
    with pytest.raises(ValueError):
        calcular_total([("18:00", "08:00")])


def test_formato_invalido_deve_gerar_erro():
    with pytest.raises(ValueError):
        calcular_total([("8h", "12:00")])


def test_formato_invalido_minutos_negativos_ou_acima_de_59():
    with pytest.raises(ValueError):
        calcular_total([("8h:-1", "12:00")])
    with pytest.raises(ValueError):
        calcular_total([("08:00", "12:60")])


def test_formato_invalido_horas_negativas():
    with pytest.raises(ValueError):
        calcular_total([("-01:00", "12:00")])
