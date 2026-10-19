# controller/controlador_mm1.py
# ------------------------------------------------------------
# El controlador une el MODELO con la VISTA.
# - Pide opcion a la vista.
# - Pide escenario a la fabrica.
# - Calcula teoria (modelo).
# - Ejecuta simulacion (modelo).
# - Muestra resultados y graficas (vista).
# ------------------------------------------------------------

from Model.teoria_mm1 import TeoriaMM1
from Model.simulacion_mm1 import ejecutar_replicaciones
from View.vista_mm1 import VistaMM1
from Controller.factory_escenarios import FactoryEscenarios


class ControladorMM1:

    def __init__(self):
        # Instanciamos la vista y la fabrica
        self.vista = VistaMM1()
        self.factory = FactoryEscenarios()

    def ejecutar(self):
        # Bucle principal del programa
        while True:
            self.vista.mostrar_menu()
            opcion = self.vista.pedir_opcion()

            if opcion == 0:
                self.vista.mostrar_mensaje("Saliendo del programa...")
                break

            # Pedimos a la fabrica el escenario correspondiente
            datos = self.factory.crear_escenario(opcion)

            if datos is None:
                self.vista.mostrar_mensaje("Opcion invalida, intenta de nuevo.")
                continue

            # 1) Calculamos los valores teoricos
            teoria = TeoriaMM1(datos["lambd"], datos["mu"])

            if not teoria.verificar_estabilidad():
                self.vista.mostrar_mensaje("El sistema NO es estable (lambda >= mu).")
                continue

            metricas_teoricas = teoria.obtener_todas_las_metricas()

            # 2) Ejecutamos la simulacion con SimPy (varias replicas)
            #    - tiempo_total largo: cerca de la saturacion (lambda->mu) la cola
            #      tarda mucho en alcanzar su valor estacionario.
            #    - calentamiento: descarta el transitorio inicial (sistema vacio).
            #    - 3 replicas: una sola corrida cerca de lambda=mu tiene mucha
            #      varianza; el promedio de replicas es el metodo estandar.
            self.vista.mostrar_mensaje(
                "Ejecutando simulacion (3 replicas en paralelo), un momento..."
            )
            metricas_simuladas, cola_serie, espera_serie = ejecutar_replicaciones(
                datos["lambd"], datos["mu"],
                tiempo_total=50000,
                calentamiento=5000,
                repeticiones=3,
                semilla=42,
            )
            print("Simulacion finalizada.\n")

            # 3) Mostramos la tabla comparativa
            self.vista.mostrar_tabla_comparativa(
                datos["nombre"], metricas_teoricas.a_dict(), metricas_simuladas
            )

            # 4) Mostramos las graficas en una sola ventana
            self.vista.graficar_resultados(cola_serie, espera_serie)


if __name__ == "__main__":
    app = ControladorMM1()
    app.ejecutar()