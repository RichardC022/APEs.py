import os
import sys

import numpy as np
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from model import (
    Parametros,
    validar_parametros,
    construir_vector_tiempo,
    modelo_deterministico,
    modelo_discreto,
    modelo_estocastico,
    modelo_euler,
)
from controller import ejecutar_simulacion


P0, R, SIGMA, T, DT, SEED = 1000.0, 0.10, 20.0, 6.0, 0.1, 42


def test_los_cuatro_modelos_producen_resultados():
    t = construir_vector_tiempo(T, DT)
    n = len(t) - 1
    assert modelo_deterministico(P0, R, t).shape == t.shape
    assert modelo_discreto(P0, R, n).shape == (n + 1,)
    assert modelo_estocastico(P0, R, SIGMA, n, SEED).shape == (n + 1,)
    assert modelo_euler(P0, R, DT, n).shape == (n + 1,)


def test_primer_valor_coincide_con_P0():
    t = construir_vector_tiempo(T, DT)
    n = len(t) - 1
    assert modelo_deterministico(P0, R, t)[0] == P0
    assert modelo_discreto(P0, R, n)[0] == P0
    assert modelo_estocastico(P0, R, SIGMA, n, SEED)[0] == P0
    assert modelo_euler(P0, R, DT, n)[0] == P0


def test_deterministico_coincide_con_formula_exponencial():
    t = construir_vector_tiempo(T, DT)
    assert np.allclose(modelo_deterministico(P0, R, t), P0 * np.exp(R * t))


def test_discreto_cumple_recurrencia():
    n = 5
    P = modelo_discreto(P0, R, n)
    for i in range(n):
        assert P[i + 1] == pytest.approx(P[i] + R * P[i])


def test_euler_cumple_recurrencia():
    n = 5
    P = modelo_euler(P0, R, DT, n)
    for i in range(n):
        assert P[i + 1] == pytest.approx(P[i] + DT * R * P[i])


def test_sigma_cero_no_incorpora_ruido():
    n = 10
    P = modelo_estocastico(P0, R, 0.0, n, SEED)
    for i in range(n):
        assert P[i + 1] == pytest.approx(P[i] + R * P[i])


def test_misma_semilla_mismos_resultados():
    n = 10
    P1 = modelo_estocastico(P0, R, SIGMA, n, SEED)
    P2 = modelo_estocastico(P0, R, SIGMA, n, SEED)
    assert np.array_equal(P1, P2)


def test_estocastico_nunca_negativo():
    n = 10
    P = modelo_estocastico(P0, -0.9, 500.0, n, SEED)
    assert np.all(P >= 0)


def test_tiempo_y_poblacion_misma_longitud():
    t = construir_vector_tiempo(T, DT)
    n = len(t) - 1
    assert len(t) == len(modelo_deterministico(P0, R, t))
    assert len(t) == len(modelo_discreto(P0, R, n))
    assert len(t) == len(modelo_estocastico(P0, R, SIGMA, n, SEED))
    assert len(t) == len(modelo_euler(P0, R, DT, n))


def test_parametros_invalidos_generan_errores():
    with pytest.raises(ValueError):
        validar_parametros(Parametros(P0=-1, r=R, sigma=SIGMA, T=T, dt=DT, seed=SEED))
    with pytest.raises(ValueError):
        validar_parametros(Parametros(P0=P0, r=R, sigma=SIGMA, T=0, dt=DT, seed=SEED))
    with pytest.raises(ValueError):
        validar_parametros(Parametros(P0=P0, r=R, sigma=SIGMA, T=T, dt=0, seed=SEED))
    with pytest.raises(ValueError):
        validar_parametros(Parametros(P0=P0, r=R, sigma=-1, T=T, dt=DT, seed=SEED))
    with pytest.raises(TypeError):
        validar_parametros(Parametros(P0="mil", r=R, sigma=SIGMA, T=T, dt=DT, seed=SEED))
    with pytest.raises(ValueError):
        validar_parametros(Parametros(P0=P0, r=R, sigma=SIGMA, T=1.0, dt=2.0, seed=SEED))


def test_casos_r_cero_positivo_y_negativo():
    t = construir_vector_tiempo(T, DT)
    n = len(t) - 1
    assert np.allclose(modelo_deterministico(P0, 0.0, t), P0)
    assert modelo_deterministico(P0, R, t)[-1] > P0
    assert modelo_deterministico(P0, -R, t)[-1] < P0


def test_se_generan_png_y_csv(tmp_path):
    parametros = Parametros(P0=P0, r=R, sigma=SIGMA, T=T, dt=DT, seed=SEED)
    resultado = ejecutar_simulacion(parametros, str(tmp_path), mostrar=False, imprimir=False)
    assert len(resultado.t) == len(resultado.P_deterministico)

    for nombre in [
        "comparacion.csv",
        "deterministico.csv",
        "discreto.csv",
        "estocastico.csv",
        "euler.csv",
        "datos_guia.csv",
        "comparacion_modelos.png",
        "estocastico.png",
        "euler_vs_deterministico.png",
        "datos_guia.png",
        "panel_modelos.png",
    ]:
        ruta = tmp_path / nombre
        assert ruta.exists(), f"Falta {nombre}"
        assert ruta.stat().st_size > 0, f"{nombre} está vacío"
