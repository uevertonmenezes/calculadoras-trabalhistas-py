from calculadoras_trabalhistas.ferias import calcular_ferias, AbonoPecuniario, AdiantarDecimo
import pytest


def test_calculo_basico_sem_abono():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0,
        dias_ferias=30,
        abono_pecuniario=AbonoPecuniario.nao,
        adiantar_decimo=AdiantarDecimo.nao,
        dependentes=0
    )

    assert resultado["valor_proporcional"] > 0
    assert resultado["terco_ferias"] == round(resultado["valor_proporcional"] / 3, 2)
    assert resultado["desconto_inss"] >= 0
    assert resultado["desconto_irpf"] >= 0


def test_com_abono_pecuniario():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0,
        dias_ferias=30,
        abono_pecuniario=AbonoPecuniario.sim,
        adiantar_decimo=AdiantarDecimo.nao,
        dependentes=0
    )

    assert resultado["abono_pecuniario"] > 0
    assert resultado["terco_abono_pecuniario"] == round(resultado["abono_pecuniario"] / 3, 2)


def test_com_adiantamento_decimo():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0,
        dias_ferias=30,
        abono_pecuniario=AbonoPecuniario.nao,
        adiantar_decimo=AdiantarDecimo.sim,
        dependentes=0
    )

    assert resultado["adiantamento_parcela_decimo"] == 1500


def test_salario_negativo():
    with pytest.raises(ValueError):
        calcular_ferias(
            salario_bruto=-1000,
            media_horas_extras=0,
            dias_ferias=30,
            abono_pecuniario=AbonoPecuniario.nao,
            adiantar_decimo=AdiantarDecimo.nao,
            dependentes=0
        )


def test_dias_invalidos():
    with pytest.raises(ValueError):
        calcular_ferias(
            salario_bruto=3000,
            media_horas_extras=0,
            dias_ferias=40,
            abono_pecuniario=AbonoPecuniario.nao,
            adiantar_decimo=AdiantarDecimo.nao,
            dependentes=0
        )


def test_ferias_proporcional():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0,
        dias_ferias=15,
        abono_pecuniario=AbonoPecuniario.nao,
        adiantar_decimo=AdiantarDecimo.nao,
        dependentes=0
    )

    assert resultado["valor_proporcional"] == pytest.approx(1500, 0.01)


def test_valor_final_calculo_manual():
    resultado = calcular_ferias(
        salario_bruto=3000,
        media_horas_extras=0,
        dias_ferias=30,
        abono_pecuniario=AbonoPecuniario.nao,
        adiantar_decimo=AdiantarDecimo.nao,
        dependentes=0
    )

    bruto = 3000 + 1000
    liquido_esperado = (
        bruto
        - resultado["desconto_inss"]
        - resultado["desconto_irpf"]
    )

    assert resultado["valor_ferias"] == round(liquido_esperado, 2)


def test_dependentes_reduzem_irpf():
    sem_dependentes = calcular_ferias(
        5000, 0, 30,
        AbonoPecuniario.nao,
        AdiantarDecimo.nao,
        dependentes=0
    )

    com_dependentes = calcular_ferias(
        5000, 0, 30,
        AbonoPecuniario.nao,
        AdiantarDecimo.nao,
        dependentes=2
    )

    assert com_dependentes["desconto_irpf"] <= sem_dependentes["desconto_irpf"]


def test_media_horas_extras_influencia_valor():
    sem_extra = calcular_ferias(3000, 0, 30,
                                AbonoPecuniario.nao,
                                AdiantarDecimo.nao)

    com_extra = calcular_ferias(3000, 500, 30,
                                AbonoPecuniario.nao,
                                AdiantarDecimo.nao)

    assert com_extra["valor_proporcional"] > sem_extra["valor_proporcional"]


def test_tipo_abono_pecuniario():
    with pytest.raises(TypeError):
        calcular_ferias(
            3000, 0, 30,
            "sim",
            AdiantarDecimo.nao
        )


def test_media_horas_extras_negativa():
    with pytest.raises(ValueError):
        calcular_ferias(
            3000, -100, 30,
            AbonoPecuniario.nao,
            AdiantarDecimo.nao
        )


def test_dependentes_negativo():
    with pytest.raises(ValueError):
        calcular_ferias(
            3000, 0, 30,
            AbonoPecuniario.nao,
            AdiantarDecimo.nao,
            dependentes=-1
        )


def test_valor_ferias_nunca_negativo():
    resultado = calcular_ferias(
        3000, 0, 30,
        AbonoPecuniario.nao,
        AdiantarDecimo.nao
    )

    assert resultado["valor_ferias"] >= 0