import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import Parametros
from controller import ejecutar_simulacion


def parsear_argumentos(argv=None) -> Parametros:
    parser = argparse.ArgumentParser(
        description="Simulación y comparación de modelos de crecimiento poblacional (MVC)."
    )
    parser.add_argument("--P0", type=float, default=1000.0,
                        help="Población inicial (>= 0). Por defecto 1000.")
    parser.add_argument("--r", type=float, default=0.10,
                        help="Tasa de crecimiento. Por defecto 0.10.")
    parser.add_argument("--sigma", type=float, default=20.0,
                        help="Desviación estándar del ruido (>= 0). Por defecto 20.")
    parser.add_argument("--T", type=float, default=6.0,
                        help="Tiempo total (> 0). Por defecto 6.")
    parser.add_argument("--dt", type=float, default=0.1,
                        help="Paso temporal (> 0). Por defecto 0.1.")
    parser.add_argument("--seed", type=int, default=42,
                        help="Semilla aleatoria. Por defecto 42.")
    parser.add_argument("--no-show", action="store_true",
                        help="No abrir las gráficas en ventana (solo guardar PNG).")
    parser.add_argument("--no-print", action="store_true",
                        help="No imprimir las tablas en la terminal.")
    args = parser.parse_args(argv)
    parametros = Parametros(P0=args.P0, r=args.r, sigma=args.sigma, T=args.T, dt=args.dt, seed=args.seed)
    return parametros, (not args.no_show), (not args.no_print)


def main(argv=None) -> int:
    parametros, mostrar, imprimir = parsear_argumentos(argv)
    raiz = os.path.dirname(os.path.abspath(__file__))
    directorio_resultados = os.path.join(raiz, "resultados")
    try:
        ejecutar_simulacion(parametros, directorio_resultados,
                            mostrar=mostrar, imprimir=imprimir)
    except (ValueError, TypeError) as exc:
        print(f"Error en los parámetros: {exc}", file=sys.stderr)
        return 1
    print("Simulación completada.")
    print(f"Resultados en: {directorio_resultados}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
