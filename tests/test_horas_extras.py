import pytest

from calculadoras_trabalhistas.horas_extras import calcular_horas_extras


# BASES PADRÃO #

SALARIO_BASE = 1621
HORA_MES_PADRAO = 220

HORA_0 = "00:00"
HORA_1 = "01:00"
HORA_INVALIDA = "2H"


# CASOS BÁSICOS #

def test_calculo_basico_deve_retornar_valores_corretos():
    resultado = calcular_horas_extras(
        salario_bruto=SALARIO_BASE,
        hora_mes=HORA_MES_PADRAO,
        hora_extra50=HORA_1,
        hora_extra100=HORA_1,
        hora_noturna=HORA_1
    )

    assert resultado["valor_hora_trabalhada"] == pytest.approx(7.37, 0.01)
    assert resultado["total_hora_extra50"] == pytest.approx(11.05, 0.01)
    assert resultado["total_hora_extra100"] == pytest.approx(14.74, 0.01)
    assert resultado["total_hora_noturna"] == pytest.approx(13.26, 0.01)
    assert resultado["total_geral"] == pytest.approx(39.05, 0.01)


# FORMATO DE HORAS #

@pytest.mark.parametrize(
    "hora_valida, hora_invalida",
    [
        (HORA_1, HORA_INVALIDA),
        (HORA_0, "25:00"),
        (HORA_0, "-01:00"),
        (HORA_0, "00:60"),
        (HORA_0, "abc"),
    ]
)
def test_formato_hora_invalido_deve_gerar_erro(hora_valida, hora_invalida):
    with pytest.raises(ValueError):
        calcular_horas_extras(
            salario_bruto=2200,
            hora_mes=HORA_MES_PADRAO,
            hora_extra50=hora_invalida,
            hora_extra100=hora_valida,
            hora_noturna=hora_valida
        )


# SEM HORAS EXTRAS #

def test_sem_horas_extras_total_deve_ser_zero():
    resultado = calcular_horas_extras(
        salario_bruto=3000,
        hora_mes=HORA_MES_PADRAO,
        hora_extra50=HORA_0,
        hora_extra100=HORA_0,
        hora_noturna=HORA_0
    )

    assert resultado["total_geral"] == pytest.approx(0.0, 0.01)


# ESTRUTURA DO RETORNO #

def test_estrutura_de_retorno_deve_ser_dicionario_com_chaves_esperadas():
    resultado = calcular_horas_extras(
        salario_bruto=2000,
        hora_mes=HORA_MES_PADRAO,
        hora_extra50=HORA_1,
        hora_extra100=HORA_0,
        hora_noturna=HORA_0
    )

    assert isinstance(resultado, dict)
    chaves_esperadas = [
        "valor_hora_trabalhada",
        "total_hora_extra50",
        "total_hora_extra100",
        "total_hora_noturna",
        "total_geral"
    ]
    for chave in chaves_esperadas:
        assert chave in resultado


# VALORES EXTREMOS / DECIMAIS #

def test_valores_decimais_deve_funcionar_corretamente():
    resultado = calcular_horas_extras(
        salario_bruto=2500.75,
        hora_mes=HORA_MES_PADRAO,
        hora_extra50="02:30",
        hora_extra100="01:45",
        hora_noturna="00:15"
    )

    # Apenas validar que valores não são negativos e total geral bate.
    assert resultado["total_geral"] >= 0
    total_calculado = (
        resultado["total_hora_extra50"]
        + resultado["total_hora_extra100"]
        + resultado["total_hora_noturna"]
    )
    assert resultado["total_geral"] == pytest.approx(total_calculado, 0.01)
