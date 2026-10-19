import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Permite funcionar sin pantalla (servidores/CI). Si hay display, matplotlib
# usará automáticamente un backend interactivo.
if not os.environ.get("DISPLAY") and os.name != "nt":
    matplotlib.use("Agg")


def _asegurar_directorio(ruta: str) -> None:
    directorio = os.path.dirname(ruta)
    if directorio:
        os.makedirs(directorio, exist_ok=True)


def _graficar_comparacion(ax, t, P_det, P_disc, P_est, P_eul) -> None:
    ax.plot(t, P_det, "-", linewidth=2, label="Determinístico")
    ax.plot(t, P_disc, "o-", markersize=3, label="Discreto")
    ax.plot(t, P_est, ".", markersize=3, alpha=0.6, label="Estocástico")
    ax.plot(t, P_eul, "--", label="Euler (continuo)")
    ax.set_title("Comparación de los cuatro modelos")
    ax.set_xlabel("Tiempo (t)")
    ax.set_ylabel("Población P(t)")
    ax.grid(True, alpha=0.3)
    ax.legend()


def _graficar_estocastico(ax, t, P_est) -> None:
    ax.plot(t, P_est, "-o", markersize=2, color="tab:red", label="Estocástico")
    ax.set_title("Comportamiento del modelo estocástico")
    ax.set_xlabel("Tiempo (t)")
    ax.set_ylabel("Población P(t)")
    ax.grid(True, alpha=0.3)
    ax.legend()


def _graficar_euler(ax, t, P_det, P_eul) -> None:
    ax.plot(t, P_det, "-", linewidth=2, label="Continuo exacto")
    ax.plot(t, P_eul, "--", label="Euler (aproximación)")
    ax.set_title("Continuo exacto vs aproximación de Euler")
    ax.set_xlabel("Tiempo (t)")
    ax.set_ylabel("Población P(t)")
    ax.grid(True, alpha=0.3)
    ax.legend()


def _graficar_observaciones(ax, datos) -> None:
    t = np.arange(len(datos))
    ax.plot(t, datos, "s-", color="tab:green", label="Observaciones de la guía")
    ax.set_title("Datos de entrada de la guía")
    ax.set_xlabel("Índice temporal")
    ax.set_ylabel("Población observada")
    ax.grid(True, alpha=0.3)
    ax.legend()


def figura_panel_completo(t, P_det, P_disc, P_est, P_eul, datos, ruta_png: str):
    """Crea UNA figura con los cuatro gráficos en una cuadrícula 2x2.

    Se guarda como PNG y se deja abierta para mostrarse en una sola ventana.
    """
    _asegurar_directorio(ruta_png)
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Simulación de crecimiento poblacional: comparación de modelos", fontsize=14)
    _graficar_comparacion(axes[0, 0], t, P_det, P_disc, P_est, P_eul)
    _graficar_estocastico(axes[0, 1], t, P_est)
    _graficar_euler(axes[1, 0], t, P_det, P_eul)
    _graficar_observaciones(axes[1, 1], datos)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(ruta_png)
    return fig


def guardar_graficas_individuales(t, P_det, P_disc, P_est, P_eul, datos, directorio: str) -> None:
    """Guarda cada gráfico como PNG separado (figuras cerradas, sin mostrarse)."""
    fig, ax = plt.subplots(figsize=(9, 5))
    _graficar_comparacion(ax, t, P_det, P_disc, P_est, P_eul)
    fig.tight_layout()
    fig.savefig(os.path.join(directorio, "comparacion_modelos.png"))
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    _graficar_estocastico(ax, t, P_est)
    fig.tight_layout()
    fig.savefig(os.path.join(directorio, "estocastico.png"))
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    _graficar_euler(ax, t, P_det, P_eul)
    fig.tight_layout()
    fig.savefig(os.path.join(directorio, "euler_vs_deterministico.png"))
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    _graficar_observaciones(ax, datos)
    fig.tight_layout()
    fig.savefig(os.path.join(directorio, "datos_guia.png"))
    plt.close(fig)


def _desactivar_reporte_foco() -> None:
    """Desactiva el modo DEC 1004 (reporte de foco) del terminal.

    Si está activo, el terminal envía CSI I / CSI O al ganar/perder foco y,
    con el 'echo' del tty activado, esos bytes aparecen impresos en pantalla
    como `^[[I` / `^[[O` al abrir la ventana gráfica. Enviar la secuencia de
    desactivación evita ese ruido. Es inofensivo si ya estaba desactivado.
    """
    import sys
    if sys.stdout.isatty():
        sys.stdout.write("\x1b[?1004l")
        sys.stdout.flush()


def mostrar_graficas() -> None:
    """Muestra en pantalla todas las figuras abiertas (bloquea hasta cerrarlas)."""
    import sys
    sys.stdout.flush()
    _desactivar_reporte_foco()
    if matplotlib.get_backend().lower() == "agg":
        print("(Aviso) No hay entorno gráfico disponible; las figuras se guardaron como PNG.",
              flush=True)
        return
    print("Abriendo la ventana con las gráficas (ciérrala para terminar)...", flush=True)
    plt.show()


def cerrar_graficas() -> None:
    plt.close("all")


def guardar_csv(ruta_csv: str, columnas: dict) -> None:
    _asegurar_directorio(ruta_csv)
    arreglos = [np.asarray(v, dtype=float) for v in columnas.values()]
    longitud = max(len(a) for a in arreglos)
    arreglos = [
        np.pad(a, (0, longitud - len(a)), constant_values=np.nan) if len(a) < longitud else a
        for a in arreglos
    ]
    matriz = np.column_stack(arreglos)
    encabezado = ",".join(columnas.keys())
    np.savetxt(ruta_csv, matriz, delimiter=",", header=encabezado, comments="")
