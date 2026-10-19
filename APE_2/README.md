# APE_2 — Simulación de crecimiento poblacional (MVC)

## 1. Descripción del proyecto

Aplicación de línea de comandos en Python que implementa y compara **cuatro
modelos de crecimiento poblacional** exponencial dentro de un mismo horizonte
temporal:

| Modelo | Ecuación | Tipo |
|---|---|---|
| Determinístico | `P(t) = P0 * exp(r * t)` | Continuo exacto |
| Discreto | `P[n+1] = P[n] + r * P[n]` | Pasos enteros de tiempo |
| Estocástico | `P[n+1] = max(0, P[n] + r*P[n] + ruido)`, `ruido ~ N(0, sigma)` | Con aleatoriedad |
| Euler | `P[n+1] = P[n] + dt * r * P[n]` | Aproximación numérica de `dP/dt = r * P` |

**Problema que resuelve:** permite observar cómo la misma tasa de crecimiento
produce trayectorias distintas según se modele el tiempo de forma continua o
discreta, con o sin ruido aleatorio, y qué tan buena es la aproximación
numérica de Euler frente a la solución analítica.

**Funcionalidades principales:**

- Valida los parámetros de entrada (`P0`, `r`, `sigma`, `T`, `dt`, `seed`)
  antes de simular.
- Ejecuta los cuatro modelos sobre un vector de tiempo común (`n = T / dt`).
- Imprime en terminal tablas comparativas, un resumen estadístico
  (inicial/final/mínimo/máximo) y las observaciones de la guía.
- Genera gráficas PNG (panel único 2x2 e imágenes individuales) y exporta los
  resultados a CSV.
- Es reproducible: el modelo estocástico usa `numpy.random.default_rng(seed)`,
  así que la misma semilla produce exactamente los mismos resultados.
- Incluye pruebas automatizadas con pytest.

El código sigue el patrón **Modelo-Vista-Controlador (MVC)**: los modelos
matemáticos y la validación viven en `model/`, la orquestación en
`controller/` y la presentación (gráficas y tablas) en `view/`.

## 2. Tecnologías utilizadas

| Tecnología | Versión requerida | Uso |
|---|---|---|
| Python | 3.10 o superior | Lenguaje de programación (el entorno local usa 3.14) |
| [numpy](requirements.txt) | — | Arreglos, `linspace`, exponenciales y generación de números aleatorios (`default_rng`) |
| [matplotlib](requirements.txt) | — | Gráficas PNG (panel 2x2 e individuales) y ventana de visualización |
| [pytest](requirements.txt) | — | Pruebas automatizadas de los modelos, la validación y la exportación de archivos |

No hay frameworks web, bases de datos ni servicios externos: es una
aplicación de escritorio/CLI. Las dependencias se declaran únicamente en
`requirements.txt`.

## 3. Instalación y configuración

**Requisitos previos:**

- Python 3.10 o superior (`python --version`)
- `pip` y `venv` incluidos en la distribución de Python

**Pasos:**

```bash
cd APE_2
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

`requirements.txt` instala `numpy`, `matplotlib` y `pytest`.

**Configuración:**

- No se requieren variables de entorno, archivos de configuración ni
  credenciales.
- No hay base de datos: los resultados se guardan como archivos en la carpeta
  `resultados/`, que el programa crea automáticamente si no existe.
- Todos los parámetros de la simulación se pasan por línea de comandos (ver
  sección 4); los valores por defecto están definidos en
  `model/parametros.py` (`Parametros`).

## 4. Uso y ejecución

**Ejecución principal** (abre una ventana con un panel 2x2; ciérrala para
terminar el programa):

```bash
python main.py
```

Al ejecutar se:

1. Imprime en terminal las tablas de los cuatro modelos, el resumen
   estadístico y los datos de entrada de la guía.
2. Muestra una sola ventana con los cuatro gráficos en un panel 2x2.
3. Guarda todos los PNG y CSV en `resultados/`.

**Parámetros disponibles** (todos opcionales):

```bash
python main.py --P0 1000 --r 0.10 --sigma 20 --T 6 --dt 0.1 --seed 42
```

| Argumento | Descripción | Por defecto |
|---|---|---|
| `--P0` | Población inicial (>= 0) | `1000` |
| `--r` | Tasa de crecimiento | `0.10` |
| `--sigma` | Desviación estándar del ruido (>= 0) | `20` |
| `--T` | Tiempo total (> 0) | `6` |
| `--dt` | Paso temporal (> 0) | `0.1` |
| `--seed` | Semilla aleatoria (reproducibilidad) | `42` |
| `--no-show` | No abre ventanas, solo guarda los PNG | — |
| `--no-print` | No imprime las tablas en terminal | — |

Ejemplo sin entorno gráfico (servidores, CI):

```bash
python main.py --no-show
```

Los parámetros inválidos (por ejemplo `--P0 -5`, `--dt 0` o `--sigma -1`)
detienen la ejecución con un mensaje de error en `stderr` y código de salida
`1`.

**Pruebas:**

```bash
pytest -v
```

**Salidas generadas en `resultados/`:**

- Gráficas: `panel_modelos.png` (panel 2x2 mostrado en ventana),
  `comparacion_modelos.png`, `estocastico.png`,
  `euler_vs_deterministico.png`, `datos_guia.png`.
- Datos: `comparacion.csv`, `deterministico.csv`, `discreto.csv`,
  `estocastico.csv`, `euler.csv`, `datos_guia.csv`.

## 5. Estructura del proyecto

```
APE_2/
├── main.py                  # Punto de entrada: CLI con argparse, crea Parametros
├── requirements.txt         # Dependencias: numpy, matplotlib, pytest
├── README.md
├── model/
│   ├── __init__.py          # Exporta parámetros, modelos y DATOS_GUIA
│   ├── parametros.py        # DATOS_GUIA, dataclass Parametros y su validación
│   └── modelos.py           # Los cuatro modelos + construir_vector_tiempo
├── controller/
│   ├── __init__.py
│   └── controlador.py       # ejecutar_simulacion: valida, simula y exporta
├── view/
│   ├── __init__.py
│   ├── graficas.py          # Figuras matplotlib, guardado de PNG y CSV
│   └── tablas.py            # Impresión en terminal de tablas y resumen
├── tests/
│   └── test_modelos.py      # Pruebas pytest de modelos, validación y archivos
└── resultados/              # PNG y CSV generados (creada en runtime)
```

**Organización del código:**

- `model/modelos.py` — funciones puras: `modelo_deterministico`,
  `modelo_discreto`, `modelo_estocastico`, `modelo_euler` y
  `construir_vector_tiempo`. Sin efectos secundarios (salvo el RNG
  sembrado del estocástico).
- `model/parametros.py` — define `DATOS_GUIA` (observaciones de entrada de la
  guía), el dataclass inmutable `Parametros` con la propiedad `n_pasos`, y
  `validar_parametros` que lanza `ValueError`/`TypeError` ante entradas
  inválidas.
- `controller/controlador.py` — `ejecutar_simulacion` valida los parámetros,
  construye el vector de tiempo, ejecuta los cuatro modelos, exporta CSV/PNG,
  imprime las tablas y devuelve un `SimulacionResultado` con los arreglos.
- `view/graficas.py` — crea el panel 2x2 (`figura_panel_completo`), las
  gráficas individuales, `guardar_csv`, y maneja la ventana (`mostrar_graficas`)
  con backend `Agg` automático cuando no hay display.
- `view/tablas.py` — formateo de las tablas comparativa, de datos de la guía y
  del resumen estadístico.
- `main.py` — parsea los argumentos de línea de comandos y llama al
  controlador; no contiene lógica de negocio.
- `tests/test_modelos.py` — verifica longitudes, valores iniciales iguales a
  `P0`, recurrencias, `sigma = 0`, reproducibilidad por semilla, ausencia de
  valores negativos, validación de parámetros y generación de los 11 archivos
  de salida.
