
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib
matplotlib.use("TkAgg")

from Controller.controller import ControladorLluvia

def main():
    controlador = ControladorLluvia()
    controlador.ejecutar()

if __name__ == "__main__":
    main()
