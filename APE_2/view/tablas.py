def _formatear_tabla(encabezados, filas, ancho=14) -> str:
    formatos = [f"{{:>{ancho}}}" for _ in encabezados]
    linea_encabezado = " | ".join(fmt.format(h) for fmt, h in zip(formatos, encabezados))
    separador = "-+-".join("-" * ancho for _ in encabezados)
    lineas = [linea_encabezado, separador]
    for fila in filas:
        celdas = [f"{valor:.2f}" if isinstance(valor, float) else str(valor) for valor in fila]
        lineas.append(" | ".join(fmt.format(c) for fmt, c in zip(formatos, celdas)))
    return "\n".join(lineas)


def imprimir_tabla_modelos(t, P_det, P_disc, P_est, P_eul) -> None:
    print("\n=== Comparación de los cuatro modelos ===")
    print(f"{'t':>8} | {'Determinístico':>15} | {'Discreto':>15} | {'Estocástico':>15} | {'Euler':>15}")
    print("-" * 84)
    for i in range(len(t)):
        print(f"{t[i]:>8.2f} | {P_det[i]:>15.2f} | {P_disc[i]:>15.2f} | {P_est[i]:>15.2f} | {P_eul[i]:>15.2f}")


def imprimir_datos_guia(datos) -> None:
    print("\n=== Datos de entrada de la guía (observaciones, no resultados de modelos) ===")
    print(f"{'índice':>8} | {'Población observada':>22}")
    print("-" * 34)
    for i, valor in enumerate(datos):
        print(f"{i:>8} | {float(valor):>22.2f}")


def imprimir_resumen_estadistico(P_det, P_disc, P_est, P_eul, P0) -> None:
    print("\n=== Resumen (valor inicial, final, mínimo y máximo) ===")
    nombres = ["Determinístico", "Discreto", "Estocástico", "Euler"]
    for nombre, serie in zip(nombres, [P_det, P_disc, P_est, P_eul]):
        print(f"{nombre:>15}: inicial={serie[0]:.2f}  final={serie[-1]:.2f}  "
              f"min={serie.min():.2f}  max={serie.max():.2f}")
