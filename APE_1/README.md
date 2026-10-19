# APE_1 — Modelo de Predicción de Lluvia

## 1. Descripción del proyecto

Este proyecto implementa un modelo matemático para predecir la probabilidad de lluvia a partir de tres variables: humedad, nubosidad y temperatura. La solución se desarrolla bajo el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** en Python, lo que separa la lógica de cálculo, la presentación (tabla y gráficas) y el control del flujo de ejecución. 

El sistema calcula un índice de lluvia ponderado, clasifica las condiciones para cada hora registrada y permite comparar el modelo original con un modelo ajustado mediante modificación de los pesos.

## 2. Tecnologías utilizadas

- **Python** (3.10+; recomendado 3.11+) — Lenguaje principal para implementar el modelo, la vista y el controlador.
- **NumPy** (2.5.3) — Manipulación de arreglos numéricos y cálculos vectorizados.
- **Matplotlib** (3.11.2) — Generación de gráficas y visualización de resultados; se configura para utilizar el backend `TkAgg`.
- **Tkinter** — Interfaz gráfica para mostrar las ventanas de las gráficas (proporcionado por la instalación estándar de Python).

## 3. Instalación

### Requisitos previos

- Tener instalado Python 3.10 o superior.
- Tener instalado pip (gestor de paquetes de Python).
- Tener instalado Git (opcional, según método de obtención del proyecto).

### Pasos de instalación

1. **Clonar el repositorio**

   Si el repositorio está disponible, clónalo desde su URL. Reemplaza `<URL_DEL_REPOSITORIO>` con la URL correspondiente.

   ```bash
   git clone https://github.com/RichardC022/APEs.py.git
   cd APE_1
   ```

2. **Crear y activar un entorno virtual**

   **En Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **En Windows (cmd):**

   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instalar las dependencias**

   Este proyecto utiliza únicamente NumPy y Matplotlib. Si no existe un archivo `requirements.txt` en la raíz del proyecto, instálalos manualmente.

   ```bash
   pip install numpy matplotlib
   ```

## 4. Uso

El punto de entrada del proyecto es `main.py` ubicado en la raíz de `APE_1`.

### Ejecución

```bash
python main.py
```

### Flujo de ejecución

Al ejecutarse, el sistema realiza las siguientes acciones:

1. **Simulación del modelo original.** Genera la tabla con todos los cálculos para cada hora (06:00 a 22:00): humedad, nubosidad, temperatura, valores normalizados (H, N), factor de temperatura (Tf), índice de lluvia (I) y estado clasificado.
2. **Visualización de resultados.** Muestra en consola la tabla completa y abre una gráfica con la evolución del índice I junto a los umbrales de clasificación.
3. **Ajuste del modelo.** Recalcula con pesos ajustados (H=0.4, N=0.4, Tf=0.2), mostrando en consola la nueva tabla y abriendo una segunda gráfica comparativa entre el modelo original y el ajustado.
4. **Presentación simultánea.** Ambas ventanas gráficas se muestran de forma simultánea mediante `plt.show()`.

### Estructura relevante para la ejecución

```text
APE_1/
├── main.py        # Punto de entrada
├── Controller/    # Controlador (conexión Modelo-Vista)
├── Modelo/        # Lógica matemática y datos
└── Vista/         # Presentación (consola + gráficas)
```

### Validaciones y restricciones

- El modelo ajustado valida que la suma de los pesos sea 1.0 (se utiliza `assert abs((w_h + w_n + w_tf) - 1.0) < 1e-9`).
- El factor de temperatura se calcula por rangos discretos (sin interpolación), según la tabla definida en el modelo.
- Los datos horarios están definidos en el modelo (`Modelo/model.py`) y no se solicitan por entrada de usuario.

## 5. Configuración

El proyecto **no requiere configuración externa** (no utiliza archivos `.env`, variables de entorno ni archivos de configuración adicionales). 

Todos los parámetros relevantes se definen directamente en el código:

- **Datos de simulación:** `Modelo/model.py` — contiene las listas/arrays de horas, humedad (%), nubosidad (%) y temperatura (°C).
- **Pesos del modelo original:** `Modelo/model.py` — `W_H = 0.5`, `W_N = 0.3`, `W_TF = 0.2`.
- **Tabla de factor de temperatura (Tf):** `Modelo/model.py` — `TABLA_TF` con los pares (Temperatura, Tf).
- **Umbrales de clasificación:** `Modelo/model.py` — implementados en el método `clasificar()` (`< 0.40`, `< 0.60`, `< 0.75`, `≥ 0.75`).
- **Backend gráfico:** `main.py` — `matplotlib.use("TkAgg")`.
