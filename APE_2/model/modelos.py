import numpy as np


def construir_vector_tiempo(T: float, dt: float) -> np.ndarray:
    if T < 0:
        raise ValueError("T debe ser >= 0")
    if dt <= 0:
        raise ValueError("dt debe ser > 0")
    n = int(round(T / dt))
    return np.linspace(0.0, T, n + 1)


def modelo_deterministico(P0: float, r: float, t: np.ndarray) -> np.ndarray:
    """P(t) = P0 * exp(r * t). No usa números aleatorios."""
    return P0 * np.exp(r * t)


def modelo_discreto(P0: float, r: float, n_pasos: int) -> np.ndarray:
    """P[n+1] = P[n] + r * P[n]. Tiempo en intervalos discretos (n = 0..n_pasos)."""
    if n_pasos < 0:
        raise ValueError("n_pasos debe ser >= 0")
    P = np.empty(n_pasos + 1, dtype=float)
    P[0] = P0
    for n in range(n_pasos):
        P[n + 1] = P[n] + r * P[n]
    return P


def modelo_estocastico(P0: float, r: float, sigma: float, n_pasos: int, seed: int) -> np.ndarray:
    """P[n+1] = max(0, P[n] + r*P[n] + ruido), ruido ~ N(0, sigma). Reproducible con la misma semilla."""
    if n_pasos < 0:
        raise ValueError("n_pasos debe ser >= 0")
    if sigma < 0:
        raise ValueError("sigma debe ser >= 0")
    rng = np.random.default_rng(int(seed))
    P = np.empty(n_pasos + 1, dtype=float)
    P[0] = P0
    for n in range(n_pasos):
        ruido = rng.normal(0.0, sigma)
        P[n + 1] = max(0.0, P[n] + r * P[n] + ruido)
    return P


def modelo_euler(P0: float, r: float, dt: float, n_pasos: int) -> np.ndarray:
    """P[n+1] = P[n] + dt * r * P[n] para dP/dt = r*P."""
    if n_pasos < 0:
        raise ValueError("n_pasos debe ser >= 0")
    if dt <= 0:
        raise ValueError("dt debe ser > 0")
    P = np.empty(n_pasos + 1, dtype=float)
    P[0] = P0
    for n in range(n_pasos):
        P[n + 1] = P[n] + dt * r * P[n]
    return P
