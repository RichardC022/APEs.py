import os
from dataclasses import dataclass

import numpy as np

from model import (
    Parametros,
    validar_parametros,
    construir_vector_tiempo,
    modelo_deterministico,
    modelo_discreto,
    modelo_estocastico,
    modelo_euler,
    DATOS_GUIA,
)
from view import (
    guardar_csv,
    guardar_graficas_individuales,
    figura_panel_completo,
    mostrar_graficas,
    cerrar_graficas,
    imprimir_tabla_modelos,
    imprimir_datos_guia,
    imprimir_resumen_estadistico,
)


@dataclass
class SimulacionResultado:
    t: np.ndarray
    P_deterministico: np.ndarray
    P_discreto: np.ndarray
    P_estocastico: np.ndarray
    P_euler: np.ndarray


def ejecutar_simulacion(parametros: Parametros, directorio_resultados: str,
                        mostrar: bool = False, imprimir: bool = True) -> SimulacionResultado:
    validar_parametros(parametros)
    os.makedirs(directorio_resultados, exist_ok=True)

    t = construir_vector_tiempo(parametros.T, parametros.dt)
    n_pasos = parametros.n_pasos

    P_det = modelo_deterministico(parametros.P0, parametros.r, t)
    P_disc = modelo_discreto(parametros.P0, parametros.r, n_pasos)
    P_est = modelo_estocastico(parametros.P0, parametros.r, parametros.sigma, n_pasos, parametros.seed)
    P_eul = modelo_euler(parametros.P0, parametros.r, parametros.dt, n_pasos)

    _exportar(t, P_det, P_disc, P_est, P_eul, directorio_resultados)

    if imprimir:
        imprimir_tabla_modelos(t, P_det, P_disc, P_est, P_eul)
        imprimir_resumen_estadistico(P_det, P_disc, P_est, P_eul, parametros.P0)
        imprimir_datos_guia(DATOS_GUIA)

    if mostrar:
        mostrar_graficas()
    cerrar_graficas()

    return SimulacionResultado(
        t=t,
        P_deterministico=P_det,
        P_discreto=P_disc,
        P_estocastico=P_est,
        P_euler=P_eul,
    )


def _exportar(t, P_det, P_disc, P_est, P_eul, directorio: str) -> None:
    guardar_csv(
        os.path.join(directorio, "comparacion.csv"),
        {
            "t": t,
            "P_deterministico": P_det,
            "P_discreto": P_disc,
            "P_estocastico": P_est,
            "P_euler": P_eul,
        },
    )
    guardar_csv(os.path.join(directorio, "deterministico.csv"), {"t": t, "P": P_det})
    guardar_csv(os.path.join(directorio, "discreto.csv"), {"t": t, "P": P_disc})
    guardar_csv(os.path.join(directorio, "estocastico.csv"), {"t": t, "P": P_est})
    guardar_csv(os.path.join(directorio, "euler.csv"), {"t": t, "P": P_eul})
    guardar_csv(
        os.path.join(directorio, "datos_guia.csv"),
        {"indice": np.arange(len(DATOS_GUIA)), "P_observada": DATOS_GUIA},
    )

    guardar_graficas_individuales(t, P_det, P_disc, P_est, P_eul, DATOS_GUIA, directorio)
    # Figura única con los cuatro gráficos en un panel 2x2 (se guarda y queda
    # abierta para mostrarse en una sola ventana).
    figura_panel_completo(t, P_det, P_disc, P_est, P_eul, DATOS_GUIA,
                          os.path.join(directorio, "panel_modelos.png"))
