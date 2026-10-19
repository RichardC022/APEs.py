
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Modelo.model import ModeloLluvia
from Vista.view import VistaLluvia


class ControladorLluvia:

    def __init__(self):
        self.modelo = ModeloLluvia().simular()
        self.vista = VistaLluvia()

    def ejecutar(self):
        # 1) Tabla completa
        filas = self.modelo.get_tabla()
        self.vista.mostrar_tabla(filas)

        # 2) Gráfica 1: índice I con umbrales
        self.vista.graficar_indice(self.modelo.horas, self.modelo.I)

        # 3) Ajuste del modelo 
        original = self.modelo.I.copy()  # copia para comparar después
        self.modelo.ajustar_pesos(w_h=0.4, w_n=0.4, w_tf=0.2)
        print("\n--- Modelo ajustado (H=0.4, N=0.4, Tf=0.2) ---")
        self.vista.mostrar_tabla(self.modelo.get_tabla())
        self.vista.graficar_ajuste(self.modelo.horas, original, self.modelo.I)

        # 4) Abre las dos ventanas a la vez
        self.vista.mostrar()

if __name__ == "__main__":
    ControladorLluvia().ejecutar()
