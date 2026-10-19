#Importamos las librerias necesarias
import simpy
import numpy as np
from concurrent.futures import ProcessPoolExecutor


class SimulacionMM1:

    def __init__(self, lambd, mu, tiempo_total=1000, calentamiento=0, semilla=None):

        self.lambd = lambd
        self.mu = mu
        self.tiempo_total = tiempo_total
        self.calentamiento = calentamiento

        # Generador NumPy: reproponible si se pasa semilla
        self.rng = np.random.default_rng(semilla)

        self.tiempos_espera = []
        self.tiempos_sistema = []
        self.tamanios_cola = []

        # Areas bajo las curvas (ponderacion por tiempo) -> L, Lq y rho simulados
        self._area_cola = 0.0
        self._area_sistema = 0.0
        self._area_ocupado = 0.0
        self._ultimo_muestreo = 0.0

    def proceso_cliente(self, env, servidor):

        llegada = env.now

        with servidor.request() as req:
            yield req

            if llegada >= self.calentamiento:
                self.tiempos_espera.append(env.now - llegada)

            tiempo_servicio = self.rng.exponential(1.0 / self.mu)
            yield env.timeout(tiempo_servicio)

            if llegada >= self.calentamiento:
                self.tiempos_sistema.append(env.now - llegada)

    def generador_llegadas(self, env, servidor):
        while True:

            tiempo_entre_llegadas = self.rng.exponential(1.0 / self.lambd)
            yield env.timeout(tiempo_entre_llegadas)
            env.process(self.proceso_cliente(env, servidor))

    def monitor(self, env, servidor, dt=None):
        # Muestrea la cola y el sistema a lo largo del tiempo (no solo en las llegadas).
        # dt se adapta al horizonte de la simulacion: con un dt fijo de 0.1 y
        # tiempo_total=50000 se generan 500000 eventos de monitoreo por replica,
        # lo que domina el costo total. Con dt ~ tiempo_total/50000 el numero de
        # eventos queda acotado sin perder precision en las medias ponderadas.
        if dt is None:
            dt = max(0.1, self.tiempo_total / 50000)
        muestras_para_grafica = max(1, int(round(20.0 / dt)))
        contador = 0
        while True:
            yield env.timeout(dt)
            t = env.now
            dur = t - self._ultimo_muestreo
            n_cola = len(servidor.queue)
            # len(servidor.users) solo cuenta al cliente en atencion (capacidad = 1),
            # por eso el total en el sistema es cola + servidor ocupado.
            n_sistema = n_cola + (1 if servidor.users else 0)

            if t >= self.calentamiento:
                self._area_cola += n_cola * dur
                self._area_sistema += n_sistema * dur
                self._area_ocupado += (1 if servidor.users else 0) * dur
                contador += 1
                if contador % muestras_para_grafica == 0:
                    self.tamanios_cola.append(n_cola)

            self._ultimo_muestreo = t

    # --------------------------------------------------------
    # Metodo principal: arranca el entorno y corre la simulacion
    # --------------------------------------------------------
    def ejecutar_simulacion(self):
        # Creamos el entorno de SimPy
        env = simpy.Environment()

        # Creamos un solo servidor (capacidad = 1) -> esto es M/M/1 (FIFO por defecto)
        servidor = simpy.Resource(env, capacity=1)

        # Arrancamos el generador de llegadas y el monitor de cola/sistema
        env.process(self.generador_llegadas(env, servidor))
        env.process(self.monitor(env, servidor))

        # Corremos la simulacion hasta el tiempo total
        env.run(until=self.tiempo_total)

        return self.obtener_metricas_simuladas()

    # --------------------------------------------------------
    # Calculamos los promedios simulados
    # --------------------------------------------------------
    def obtener_metricas_simuladas(self):
        duracion = max(self.tiempo_total - self.calentamiento, 1e-9)

        def promedio(lista):
            return sum(lista) / len(lista) if lista else 0.0

        return {
            "espera_promedio": promedio(self.tiempos_espera),   # Wq simulado
            "cola_promedio": self._area_cola / duracion,        # Lq simulado (ponderado por tiempo)
            "sistema_promedio": promedio(self.tiempos_sistema), # W simulado
            "l_promedio": self._area_sistema / duracion,        # L simulado (ponderado por tiempo)
            "rho_simulado": self._area_ocupado / duracion,      # rho simulado
            "total_clientes": len(self.tiempos_espera),
        }



def _correr_una_replica(lambd, mu, tiempo_total, calentamiento, semilla):
    # Funcion a nivel de modulo para que pueda ejecutarse en otro proceso.
    sim = SimulacionMM1(lambd, mu, tiempo_total, calentamiento, semilla=semilla)
    metricas = sim.ejecutar_simulacion()
    return metricas, list(sim.tamanios_cola), list(sim.tiempos_espera)


def ejecutar_replicaciones(lambd, mu, tiempo_total, calentamiento, repeticiones=3, semilla=42):
    """
    Corre varias réplicas independientes y promedia las métricas.
    Cerca de la saturacion (lambda -> mu) una sola corrida tiene mucha varianza;
    promediar réplicas es la forma estandar de reducir ese ruido sin sesgo.
    Las réplicas se ejecutan en paralelo (un proceso por réplica) para reducir
    el tiempo de espera del usuario.
    """
    semillas = [
        None if semilla is None else semilla + i
        for i in range(repeticiones)
    ]

    if repeticiones > 1:
        try:
            with ProcessPoolExecutor(max_workers=repeticiones) as executor:
                resultados = list(executor.map(
                    _correr_una_replica,
                    [lambd] * repeticiones,
                    [mu] * repeticiones,
                    [tiempo_total] * repeticiones,
                    [calentamiento] * repeticiones,
                    semillas,
                ))
        except Exception:
            # Si el paralelismo falla (p. ej. en algunos entornos), caemos a serie.
            resultados = [
                _correr_una_replica(lambd, mu, tiempo_total, calentamiento, s)
                for s in semillas
            ]
    else:
        resultados = [
            _correr_una_replica(lambd, mu, tiempo_total, calentamiento, s)
            for s in semillas
        ]

    metricas = [r[0] for r in resultados]
    _, serie_cola, serie_espera = resultados[0]

    promediadas = {
        clave: sum(m[clave] for m in metricas) / len(metricas)
        for clave in metricas[0]
    }
    promediadas["repeticiones"] = repeticiones
    return promediadas, serie_cola, serie_espera


if __name__ == "__main__":
    sim = SimulacionMM1(2.0, 3.0, tiempo_total=500)
    resultados = sim.ejecutar_simulacion()
    print("Metricas simuladas:")
    for k, v in resultados.items():
        print(f"  {k} = {v}")
