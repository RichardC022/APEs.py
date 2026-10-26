# Practica3_MM1 — Simulación de Colas M/M/1

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![SimPy](https://img.shields.io/badge/SimPy-4.x-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-orange)
![Licencia](https://img.shields.io/badge/licencia-MIT-lightgrey)

## 1. Descripción del proyecto

Elaboración de una aplicación de consola que calcula las métricas analíticas de un sistema de colas **M/M/1** (ρ, L, Lq, W, Wq) y las compara contra los resultados de una **simulación de eventos discretos con SimPy**, permitiendo además validar la estabilidad del sistema (λ < μ); como interfaz, ofrece un menú interactivo con tres escenarios predefinidos y visualiza la evolución de la cola y los tiempos de espera mediante gráficas de Matplotlib.

## 2. Tecnologías utilizadas

- **Python 3.10+** — lenguaje principal.
- **SimPy 4.x** — simulación de eventos discretos.
- **NumPy 2.x** — generación de variables aleatorias exponenciales (RNG con semilla).
- **Matplotlib 3.x** — gráficas de cola y tiempos de espera.
- **Librería estándar** — `dataclasses` y `typing`.
- **Git / GitHub** — control de versiones y trabajo por ramas.

> Sin base de datos, Docker ni servicios externos. No maneja credenciales ni secretos; se recomienda usar un entorno virtual aislado y no ejecutar como root.

## 3. Instalación

```bash
cd APE_3source
python3 -m venv venv
source venv/bin/activate # Linux       # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 4. Uso

```bash
python main.py
```

El menú permite elegir entre tres escenarios (estable, mayor utilización y cerca de saturación) o salir. Al seleccionar uno, muestra la tabla Teórico vs. Simulado y las gráficas. Módulos con prueba individual: `python Model/teoria_mm1.py`, `python Model/simulacion_mm1.py`.

Validaciones: parámetros > 0, estabilidad `λ < μ`, y entradas inválidas no detienen el programa.

## 5. Configuración

No requiere variables de entorno ni `.env`. La configuración vive en el código: escenarios en `Controller/factory_escenarios.py`; y en `Controller/controlador_mm1.py` el horizonte de simulación (`tiempo_total = 50000`), el descarte del transitorio inicial (`calentamiento = 5000`) y el número de réplicas independientes (`repeticiones = 3`).

## 6. Estructura del proyecto

```
APE_3/
├── main.py                  # Punto de entrada
├── requirements.txt         # Dependencias (simpy, matplotlib, numpy)
├── Docs/                    # Documentación adicional
├── Controller/              # Control: bucle principal y fábrica de escenarios
├── Model/                   # Dominio: teoría M/M/1 y simulación SimPy
└── View/                    # Presentación: menú, tabla y gráficas
```

## 7. Información adicional

- **Funcionalidades clave:** métricas analíticas M/M/1, simulación SimPy, validación de estabilidad, tabla comparativa, gráficas, escenarios preconfigurados y manejo de errores.
- **Contribución:** fork → rama `feature/...` → Pull Request a `main`.



## 8. Declaración de uso de IA

En la elaboración de este proyecto se emplearon herramientas de inteligencia artificial generativa como apoyo para la revisión de código, depuración de errores sintácticos y optimización de documentación. Todo el diseño, lógica del sistema, validación de resultados y decisiones finales fueron realizados de manera autónoma e independiente por los autores.

### 1. Prompts para explicación de conceptos teóricos

**Prompt usado (Richard — Modelo teórico):**
> "Explícame las fórmulas del modelo M/M/1 y cómo se calculan L, Lq, W y Wq."

**Prompt usado (Santiago — Simulación):**
> "Dame un ejemplo básico de simulación M/M/1 con SimPy usando simpy.Resource."

**Prompt usado (Mark — Patrón de diseño):**
> "Explícame el patrón Factory Method con un ejemplo simple en Python y cómo aplicarlo en MVC."

---

###  2. Prompts para solución de errores

**Prompt usado (Santiago — SimPy):**
> "Me sale este error en SimPy: 'TypeError: 'generator' object is not callable'. ¿Cómo lo soluciono?"

**Prompt usado (Martina — Matplotlib):**
> "Mi gráfica de matplotlib no se muestra, solo sale el mensaje 'Figure size 640x480 with 0 Axes'. ¿Qué está mal?"

**Prompt usado (Mark — Importaciones):**
> "Me sale 'ModuleNotFoundError: No module named controller'. Estoy corriendo main.py desde la raíz del proyecto. ¿Cómo lo arreglo?"

**Prompt usado (Mark — Lógica del controlador):**
> "Mi bucle while en el controlador no termina cuando el usuario elige 0. ¿Por qué pasa?"

---

###  3. Prompts para aclarar sintaxis de librerías

**Prompt usado (Santiago — SimPy):**
> "¿Cuál es la diferencia entre simpy.Resource y simpy.Store en SimPy?"

**Prompt usado (Martina— Matplotlib):**
> "Cómo graficar una lista de números con matplotlib y cómo formatear una tabla en consola en Python."

**Prompt usado (Martina — Formato de tablas):**
> "Cómo usar '{:<20}'.format() para alinear texto a la izquierda en Python."