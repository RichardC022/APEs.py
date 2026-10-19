import math
from dataclasses import dataclass

import numpy as np

# Arreglo inicial proporcionado en la guía (observaciones de entrada).
DATOS_GUIA = np.array([1000, 1100, 1250, 1400, 1600, 1850, 2100], dtype=float)


@dataclass(frozen=True)
class Parametros:
    P0: float = 1000.0
    r: float = 0.10
    sigma: float = 20.0
    T: float = 6.0
    dt: float = 0.1
    seed: int = 42

    @property
    def n_pasos(self) -> int:
        if self.dt <= 0:
            raise ValueError("dt debe ser > 0")
        n = int(round(self.T / self.dt))
        if n <= 0:
            raise ValueError("Número de pasos inválido: revisa T y dt")
        return n


def _es_numero_finito(valor, nombre: str) -> None:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"{nombre} debe ser numérico (int o float)")
    if not math.isfinite(valor):
        raise ValueError(f"{nombre} debe ser finito")


def validar_parametros(p: Parametros) -> None:
    _es_numero_finito(p.P0, "P0")
    _es_numero_finito(p.r, "r")
    _es_numero_finito(p.sigma, "sigma")
    _es_numero_finito(p.T, "T")
    _es_numero_finito(p.dt, "dt")
    if not isinstance(p.seed, (int, float)) or isinstance(p.seed, bool):
        raise TypeError("seed debe ser numérico")
    if not math.isfinite(p.seed):
        raise ValueError("seed debe ser finito")
    if p.P0 < 0:
        raise ValueError("P0 debe ser >= 0")
    if p.T <= 0:
        raise ValueError("T debe ser > 0")
    if p.dt <= 0:
        raise ValueError("dt debe ser > 0")
    if p.sigma < 0:
        raise ValueError("sigma debe ser >= 0")
    n = int(round(p.T / p.dt))
    if n <= 0:
        raise ValueError("Número de pasos inválido: revisa T y dt")
