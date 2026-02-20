import pytest

from calculadoras_trabalhistas.ferias import (
    calcular_ferias,
    calcular_verbas_ferias,
    AbonoPecuniario,
    AdiantarDecimo,
)


# BASES PADRÃO #

SALARIO_BASE = 3000
MEDIA_ZERO = 0
DIAS_PADRAO = 30


@pytest.fixture
def calcular_padrao():
    def _calcular(**overrides):
        params = dict(
            salario_bruto=SALARIO_BASE,
            media_horas_extras=MEDIA_ZERO,
            dias_ferias=DIAS_PADRAO,
            abono_pecuniario=AbonoPecuniario.nao,
            adiantar_decimo=AdiantarDecimo.nao,
            dependentes=0,
        )
        params.update(overrides)
        return calcular_ferias(**params)

    return _calcular


# CÁLCULOS BÁSICOS #

def test_calculo_basico_sem_abono_deve_calcular_terco_corretamente(calcular_padrao):
    resultado = calcular_padrao()

    assert resultado["valor_proporcional"] > 0
    assert resultado["terco_ferias"] == pytest.approx(
        resultado["valor_proporcional"] / 3, 0.01
    )
    assert resultado["desconto_inss"] >= 0
    assert resultado["desconto_irpf"] >= 0


def test_com_abono_pecuniario_deve_calcular_terco_abono(calcular_padrao):
    resultado = calcular_padrao(abono_pecuniario=AbonoPecuniario.sim)

    assert resultado["abono_pecuniario"] > 0
    assert resultado["terco_abono_pecuniario"] == pytest.approx(
        resultado["abono_pecuniario"] / 3, 0.01
    )


def test_com_adiantamento_decimo_deve_pagar_metade_salario(calcular_padrao):
    resultado = calcular_padrao(adiantar_decimo=AdiantarDecimo.sim)

    assert resultado["adiantamento_parcela_decimo"] == pytest.approx(
        SALARIO_BASE / 2, 0.01
    )


# PROPORCIONALIDADES #

@pytest.mark.parametrize(
    "dias, esperado",
    [
        (30, 3000),
        (15, 1500),
        (10, 1000),
        (1, 100),
    ]
)
def test_valor_proporcional_varios_dias(calcular_padrao, dias, esperado):
    resultado = calcular_padrao(dias_ferias=dias)
    assert resultado["valor_proporcional"] == pytest.approx(esperado, 0.01)


def test_ferias_proporcionais_15_dias(calcular_padrao):
    resultado = calcular_padrao(dias_ferias=15)
    assert resultado["valor_proporcional"] == pytest.approx(1500, 0.01)


# VALORES FINAIS #

def test_valor_final_deve_ser_bruto_menos_descontos(calcular_padrao):
    resultado = calcular_padrao()

    bruto = SALARIO_BASE + (SALARIO_BASE / 3)
    liquido_esperado = (
        bruto
        - resultado["desconto_inss"]
        - resultado["desconto_irpf"]
    )

    assert resultado["valor_ferias"] == pytest.approx(liquido_esperado, 0.01)


def test_valor_ferias_nunca_deve_ser_negativo(calcular_padrao):
    resultado = calcular_padrao()
    assert resultado["valor_ferias"] >= 0


# REGRAS TRIBUTÁRIAS #

def test_dependentes_devem_reduzir_irpf(calcular_padrao):
    sem_dependentes = calcular_padrao(dependentes=0)
    com_dependentes = calcular_padrao(dependentes=2)

    assert com_dependentes["desconto_irpf"] <= sem_dependentes["desconto_irpf"]


def test_media_horas_extras_deve_influenciar_valor(calcular_padrao):
    sem_extra = calcular_padrao()
    com_extra = calcular_padrao(media_horas_extras=500)

    assert com_extra["valor_proporcional"] > sem_extra["valor_proporcional"]


# VALIDAÇÕES #

@pytest.mark.parametrize(
    "params",
    [
        dict(salario_bruto=-1000),
        dict(dias_ferias=40),
        dict(media_horas_extras=-100),
        dict(dependentes=-1),
    ],
)
def test_valores_invalidos_devem_gerar_erro(calcular_padrao, params):
    with pytest.raises(ValueError):
        calcular_padrao(**params)


def test_tipo_abono_invalido_deve_gerar_type_error(calcular_padrao):
    with pytest.raises(TypeError):
        calcular_padrao(abono_pecuniario="sim")


# VERBAS #

def test_verbas_sem_abono():
    resultado = calcular_verbas_ferias(
        salario_bruto=SALARIO_BASE,
        media_horas_extras=MEDIA_ZERO,
        dias_ferias=DIAS_PADRAO,
        abono_pecuniario=AbonoPecuniario.nao,
    )

    assert resultado["valor_proporcional"] == 3000
    assert resultado["terco_ferias"] == 1000
    assert resultado["abono"] == 0
    assert resultado["terco_abono"] == 0


# ARREDONDAMENTO #

def test_valores_devem_ter_no_maximo_duas_casas_decimais(calcular_padrao):
    resultado = calcular_padrao(salario_bruto=3333.33)

    assert resultado["valor_proporcional"] == round(
        resultado["valor_proporcional"], 2
    )
