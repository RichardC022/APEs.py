
import numpy as np


class ModeloLluvia:
    # Modelo matemático: I = 0.5*H + 0.3*N + 0.2*Tf

    # Parámetros del modelo (pesos)
    W_H = 0.5   # peso de la humedad
    W_N = 0.3   # peso de la nubosidad
    W_TF = 0.2  # peso del factor de temperatura

    TABLA_TF = [
        (10, 1.00), (12, 0.90), (14, 0.80), (16, 0.70), (18, 0.60),
        (20, 0.50), (22, 0.40), (24, 0.30), (26, 0.20), (28, 0.10),
    ]

    def __init__(self):
        # Datos: hora, humedad (%), nubosidad (%), temperatura (°C)
        self.horas = ["06:00", "08:00", "10:00", "12:00", "14:00",
                      "16:00", "18:00", "20:00", "22:00"]
        self.humedad = np.array([65, 70, 68, 60, 75, 85, 92, 88, 80], dtype=float)
        self.nubosidad = np.array([40, 50, 45, 30, 70, 85, 95, 90, 75], dtype=float)
        self.temperatura = np.array([14, 16, 18, 22, 20, 18, 16, 17, 15], dtype=float)

        self.H = None
        self.N = None
        self.Tf = None
        self.I = None
        self.estado = None

    # ---------- Funciones del modelo ----------

    def calcular_tf(self, temp):
        # Factor de temperatura por lógica de rangos (sin interpolación)
        # La tabla es decreciente: a mayor temperatura, menor Tf
        # Cada tramo [T_i, T_{i+1}) toma el Tf de T_i; <=10 → 1.00, >=28 → 0.10
        tabla = np.array(self.TABLA_TF)
        temps, tfs = tabla[:, 0], tabla[:, 1]
        if temp <= temps[0]:
            return float(tfs[0])
        if temp >= temps[-1]:
            return float(tfs[-1])
        for i in range(len(temps) - 1):
            if temps[i] <= temp < temps[i + 1]:
                return float(tfs[i])
        return float(tfs[-1])

    def clasificar(self, indice):
        if indice < 0.40:
            return "Sin lluvia"
        elif indice < 0.60:
            return "Baja posibilidad"
        elif indice < 0.75:
            return "Lluvia probable"
        else:
            return "Lluvia"

    def simular(self):
        # Ejecuta el modelo sobre todos los datos horarios
        self.H = self.humedad / 100.0
        self.N = self.nubosidad / 100.0
        self.Tf = np.array([self.calcular_tf(t) for t in self.temperatura])
        # Índice ponderado: I = w_h*H + w_n*N + w_tf*Tf  
        self.I = self.W_H * self.H + self.W_N * self.N + self.W_TF * self.Tf
        self.estado = [self.clasificar(i) for i in self.I]
        return self  # permite encadenar ModeloLluvia().simular()

    def get_tabla(self):
        # Devuelve las filas para llenar la tabla de la guía
        filas = []
        for k in range(len(self.horas)):
            filas.append({
                "Hora": self.horas[k],
                "Humedad": int(self.humedad[k]),
                "Nubosidad": int(self.nubosidad[k]),
                "Temp.": int(self.temperatura[k]),
                "H": round(self.H[k], 2),
                "N": round(self.N[k], 2),
                "Tf": round(self.Tf[k], 2),
                "Indice": round(self.I[k], 3),
                "Estado": self.estado[k],
            })
        return filas

    def ajustar_pesos(self, w_h, w_n, w_tf):
        # Ajuste del modelo: nuevos pesos 
        assert abs((w_h + w_n + w_tf) - 1.0) < 1e-9, "Los pesos deben sumar 1"
        self.W_H, self.W_N, self.W_TF = w_h, w_n, w_tf
        # Recalcula H, N, Tf, I y estado con los nuevos pesos
        return self.simular()
