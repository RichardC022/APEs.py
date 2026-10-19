"""
Modulo encargado del calculo de las metricas teoricas para un modelo de colas M/M/1.
"""

from dataclasses import dataclass
from typing import Dict, Any, Union


@dataclass
class MetricasTeoricas:
    lambda_param: float
    mu_param: float
    rho: float
    L: float
    Lq: float
    W: float
    Wq: float

    def a_dict(self) -> Dict[str, float]:
        """Convierte las metricas a un diccionario para facilitar su uso en vistas o tablas."""
        return {
            "lambda": self.lambda_param,
            "mu": self.mu_param,
            "rho": self.rho,
            "L": self.L,
            "Lq": self.Lq,
            "W": self.W,
            "Wq": self.Wq,
        }


class TeoriaMM1:
    """Clase para calcular y validar las metricas teoricas de un sistema M/M/1"""

    def __init__(self, lambda_param: float, mu_param: float):
        if lambda_param <= 0 or mu_param <= 0:
            raise ValueError("Las tasas lambda y mu deben ser mayores que cero.")
        
        self.lambda_param = float(lambda_param)
        self.mu_param = float(mu_param)

    def es_estable(self) -> bool:
        return self.lambda_param < self.mu_param

    verificar_estabilidad = es_estable

    def calcular_utilizacion(self) -> float:
        return self.lambda_param / self.mu_param

    def calcular_metricas(self) -> MetricasTeoricas:
        if not self.es_estable():
            raise ValueError(
                f"El sistema no es estable (lambda={self.lambda_param} >= mu={self.mu_param}). "
                "La cola crecería indefinidamente"
            )

        lam = self.lambda_param
        mu = self.mu_param

        rho = self.calcular_utilizacion()
        L = lam / (mu - lam)
        Lq = (lam ** 2) / (mu * (mu - lam))
        W = 1 / (mu - lam)
        Wq = lam / (mu * (mu - lam))

        return MetricasTeoricas(
            lambda_param=lam,
            mu_param=mu,
            rho=rho,
            L=L,
            Lq=Lq,
            W=W,
            Wq=Wq
        )

    obtener_todas_las_metricas = calcular_metricas


def obtener_metricas_teoricas(lambda_param: float, mu_param: float) -> Union[Dict[str, float], None]:
    try:
        modelo = TeoriaMM1(lambda_param, mu_param)
        metricas = modelo.calcular_metricas()
        return metricas.a_dict()
    except ValueError as e:
        print(f"[Error TeoriaMM1]: {e}")
        return None


# Bloque para pruebas rapidas directas del modulo
if __name__ == "__main__":
    escenarios = [
        {"nombre": "Escenario 1 (Estable)", "lambda": 2.0, "mu": 3.0},
        {"nombre": "Escenario 2 (Mayor utilización)", "lambda": 2.5, "mu": 3.0},
        {"nombre": "Escenario 3 (Cerca de saturación)", "lambda": 2.9, "mu": 3.0},
        {"nombre": "Escenario Inestable", "lambda": 3.5, "mu": 3.0},
    ]

    print("=== PRUEBA DE CALCULOS TEORICOS M/M/1 ===\n")
    for esc in escenarios:
        print(f"--- {esc['nombre']} ---")
        try:
            modelo = TeoriaMM1(esc["lambda"], esc["mu"])
            m = modelo.calcular_metricas()
            print(f"  Utilización (rho) : {m.rho:.4f}")
            print(f"  Clientes sistema (L): {m.L:.4f}")
            print(f"  Clientes cola (Lq)  : {m.Lq:.4f}")
            print(f"  Tiempo sistema (W)  : {m.W:.4f}")
            print(f"  Tiempo cola (Wq)    : {m.Wq:.4f}")
        except ValueError as err:
            print(f"  Error: {err}")
        print()