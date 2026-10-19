
import matplotlib.pyplot as plt


class VistaLluvia:

    def mostrar_tabla(self, filas):
        # Imprime la tabla formateada en consola
        
        print(f"{'Hora':<7}{'Humedad':>9}{'Nubosidad':>9}{'Temp.':>7}"
              f"{'H':>6}{'N':>6}{'Tf':>6}{'Índice':>9}  Estado")
        print("-" * 72)
        for f in filas:
            print(f"{f['Hora']:<7}{f['Humedad']:>9}{f['Nubosidad']:>9}"
                  f"{f['Temp.']:>7}{f['H']:>6.2f}{f['N']:>6.2f}"
                  f"{f['Tf']:>6.2f}{f['Indice']:>9.3f}  {f['Estado']}")

    def graficar_indice(self, horas, indice, titulo="Índice de lluvia por hora"):
        # Gráfica principal: evolución del índice I a lo largo del día
        plt.figure(figsize=(10, 5))
        plt.plot(horas, indice, marker="o", color="tab:blue", label="Índice I")

        # Umbrales del modelo (reemplazan a la línea 'Capacidad máxima K')
        plt.axhline(y=0.40, linestyle="--", color="gray",
                    label="Umbral sin lluvia (0.40)")
        plt.axhline(y=0.60, linestyle="--", color="orange",
                    label="Umbral baja posibilidad (0.60)")
        plt.axhline(y=0.75, linestyle="--", color="red",
                    label="Umbral lluvia (0.75)")

        plt.xlabel("Hora del día")
        plt.ylabel("Índice de lluvia I")
        plt.title(titulo)
        plt.grid(True)
        plt.legend()

    def graficar_ajuste(self, horas, i_original, i_ajustado):
        # Compara el índice original vs. el índice con pesos ajustados
        plt.figure(figsize=(10, 5))
        plt.plot(horas, i_original, marker="o", label="Modelo original")
        plt.plot(horas, i_ajustado, marker="x", linestyle="--",
                 label="Modelo ajustado")
        plt.axhline(y=0.60, linestyle="--", color="orange",
                    label="Umbral lluvia probable (0.60)")
        plt.xlabel("Hora del día")
        plt.ylabel("Índice I")
        plt.title("Efecto del ajuste de parámetros (pesos)")
        plt.grid(True)
        plt.legend()

    def mostrar(self):
        # Abre todas las ventanas creadas al mismo tiempo
        plt.show()
