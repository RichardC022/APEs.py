# ------------------------------------------------------------
# Esta clase se encarga de TODA la interaccion con el usuario:
# menu, tabla comparativa y graficas con matplotlib.
# ------------------------------------------------------------

import matplotlib.pyplot as plt


class VistaMM1:

    # --------------------------------------------------------
    # Menu principal
    # --------------------------------------------------------
    def mostrar_menu(self):
        print("===================================")
        print("   SIMULACION M/M/1 CON SIMPY")
        print("===================================")
        print("1. Escenario estable           (lambda=2.0, mu=3.0)")
        print("2. Escenario mayor utilizacion (lambda=2.5, mu=3.0)")
        print("3. Escenario cerca saturacion  (lambda=2.9, mu=3.0)")
        print("0. Salir")
        print("===================================")

    def pedir_opcion(self):
        # Pedimos al usuario que elija una opcion del menu
        try:
            return int(input("Elige una opcion: "))
        except ValueError:
            return -1

    # --------------------------------------------------------
    # Tabla comparativa teorico vs simulado
    # --------------------------------------------------------
    def mostrar_tabla_comparativa(self, nombre, teorico, simulado):
        print("\n--- Resultados del escenario:", nombre, "---")
        print("{:<20} {:<15} {:<15} {:<10}".format(
            "Metrica", "Teorico", "Simulado", "Error %"))
        print("-" * 62)

        def fila(etiqueta, teo, sim):
            error = 100.0 * (sim - teo) / teo if teo else 0.0
            print("{:<20} {:<15.4f} {:<15.4f} {:+9.1f}%".format(
                etiqueta, teo, sim, error))

        fila("Rho", teorico["rho"], simulado["rho_simulado"])
        fila("L  (sistema)", teorico["L"], simulado["l_promedio"])
        fila("Lq (cola)", teorico["Lq"], simulado["cola_promedio"])
        fila("W  (sistema)", teorico["W"], simulado["sistema_promedio"])
        fila("Wq (cola)", teorico["Wq"], simulado["espera_promedio"])
        print("-" * 62)
        print("L = Lq + rho (teoria): {:.4f} = {:.4f} + {:.4f}".format(
            teorico["L"], teorico["Lq"], teorico["rho"]))
        print("L = Lq + rho (simula): {:.4f} = {:.4f} + {:.4f}".format(
            simulado["l_promedio"], simulado["cola_promedio"], simulado["rho_simulado"]))
        print("Replicas promediadas:", simulado.get("repeticiones", 1))
        print("Total de clientes simulados (promedio por replica):",
              round(simulado["total_clientes"]))
        print("Tiempo promedio de espera simulado:", round(simulado["espera_promedio"], 4))
        print("Tamanio promedio de cola simulado:", round(simulado["cola_promedio"], 4))
        print("Tamano promedio de clientes en el sistema simulado:",
              round(simulado["l_promedio"], 4))

    # --------------------------------------------------------
    # Graficas de cola y tiempos de espera en una sola ventana
    # --------------------------------------------------------
    def graficar_resultados(self, tamanios_cola, tiempos_espera):
        fig, (ax_cola, ax_espera) = plt.subplots(1, 2, figsize=(14, 4))

        ax_cola.plot(tamanios_cola, color="steelblue")
        ax_cola.set_title("Evolucion del tamanio de la cola")
        ax_cola.set_xlabel("Numero de llegada")
        ax_cola.set_ylabel("Clientes en cola")
        ax_cola.grid(True)

        ax_espera.plot(tiempos_espera, color="indianred")
        ax_espera.set_title("Tiempos de espera por cliente")
        ax_espera.set_xlabel("Cliente")
        ax_espera.set_ylabel("Tiempo de espera")
        ax_espera.grid(True)

        fig.tight_layout()
        plt.show()

    # --------------------------------------------------------
    # Mensaje generico
    # --------------------------------------------------------
    def mostrar_mensaje(self, mensaje):
        print(mensaje)


# ------------------------------------------------------------
# Bloque de prueba rapida
# ------------------------------------------------------------
if __name__ == "__main__":
    vista = VistaMM1()
    vista.mostrar_menu()
    vista.graficar_resultados(
        [0, 1, 2, 3, 2, 1, 0, 0, 1, 2],
        [0.1, 0.3, 0.2, 0.5, 0.1, 0.0, 0.4],
    )