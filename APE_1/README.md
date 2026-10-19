# APE_1 - Modelo de Predicción de Lluvia

## Descripción

Este proyecto implementa un modelo matemático para predecir la probabilidad de lluvia basado en tres variables: humedad, nubosidad y temperatura. Se desarrolla bajo el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** utilizando Python.

## Estructura del Proyecto

```
APEs.py/
├── APE_1/
│   ├── Controller/
│   │   └── controller.py   # Conecta Modelo y Vista
│   ├── Modelo/
│   │   └── model.py        # Lógica matemática y datos
│   ├── Vista/
│   │   └── view.py         # Presentación (consola + gráficas)
│   └── main.py             # Punto de entrada principal
├── .venv/                  # Entorno virtual
├── .gitignore
└── README.md
```

## Modelo Matemático

El índice de lluvia se calcula mediante la siguiente ecuación:

**I = 0.5·H + 0.3·N + 0.2·Tf**

Donde:
- **H**: Humedad relativa normalizada (Humedad % / 100)
- **N**: Nubosidad normalizada (Nubosidad % / 100)
- **Tf**: Factor de temperatura (obtenido por lógica de rangos según tabla)

**Tabla de Factor de Temperatura (Tf):**

| Temperatura (°C) | Tf |
|------------------|----|
| 10              | 1.00 |
| 12              | 0.90 |
| 14              | 0.80 |
| 16              | 0.70 |
| 18              | 0.60 |
| 20              | 0.50 |
| 22              | 0.40 |
| 24              | 0.30 |
| 26              | 0.20 |
| 28              | 0.10 |

**Regla de asignación de Tf (por rangos):** cada temperatura toma el Tf del tramo `[Tᵢ, Tᵢ₊₁)`, sin interpolación. Es decir, ≤10 °C → 1.00; [12,14) → 0.90; [14,16) → 0.80; ...; ≥28 °C → 0.10.

**Umbrales de Clasificación:**

| Índice I | Estado |
|----------|--------|
| I < 0.40 | Sin lluvia |
| 0.40 ≤ I < 0.60 | Baja posibilidad |
| 0.60 ≤ I < 0.75 | Lluvia probable |
| I ≥ 0.75 | Lluvia |

## Requisitos Previos

Antes de ejecutar el proyecto, necesitas tener instalado lo siguiente:

- **Python 3.10+** (Recomendado: 3.11 o superior)
- **pip** (gestor de paquetes de Python)
- **Git** (para clonar el repositorio)

Para verificar tu instalación:

```bash
python --version
pip --version
git --version
```

## Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd APEs.py
```

## Ejecución desde la terminal

Dentro del proyecto, activar el venv con:

```bash
source .venv/bin/activate
```

Instalar las dependencias:

```bash
pip install numpy matplotlib
```

Ejecutar el proyecto:

```bash
python -m APE_1.main
```

> Si aún no existe el entorno virtual, créalo primero con `python -m venv .venv` y luego actívalo con el comando de arriba.

## Configuración del Entorno Virtual

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

### Crear el entorno virtual

```bash
python -m venv .venv
```

### Activar el entorno virtual

**En Linux/macOS:**

```bash
source .venv/bin/activate
```

**En Windows (CMD):**

```bash
.venv\Scripts\activate.bat
```

**En Windows (PowerShell):**

```bash
.venv\Scripts\Activate.ps1
```

Al estar activado, verás `(.venv)` al inicio de tu línea de comandos.

### Desactivar el entorno virtual

```bash
deactivate
```

## Instalación de Dependencias

Este proyecto requiere las siguientes librerías:

- **numpy**: Para cálculos numéricos y manejo de arrays
- **matplotlib**: Para generar gráficas

Puedes instalarlas con el siguiente comando:

```bash
pip install numpy matplotlib
```

Verifica la instalación:

```bash
python -c "import numpy, matplotlib; print('Dependencias instaladas correctamente')"
```

## Configuración de Matplotlib

Matplotlib está configurado por defecto para mostrar las gráficas en ventanas emergentes. No requiere configuración adicional.

**Notas importantes:**
- Al ejecutar el programa, **las gráficas se abren al mismo tiempo** (una ventana por gráfica), para poder compararlas sin cerrar ninguna.
- El programa termina cuando cierras las ventanas de matplotlib.

## Ejecución del Proyecto

Tienes dos formas de ejecutar el proyecto:

### Opción 1: Desde la raíz del proyecto como módulo (recomendado)

```bash
cd APEs.py
python -m APE_1.main
```

### Opción 2: Desde el directorio del paquete

```bash
cd APE_1
python main.py
```

## ¿Qué hace el programa?

Al ejecutarse, el programa realiza lo siguiente:

1. **Muestra la tabla completa** con los datos horarios, valores normalizados, índice de lluvia y su clasificación.
2. **Genera gráfica 1**: Evolución del índice I a lo largo del día con umbrales (0.40, 0.60, 0.75).
3. **Realiza ajuste de pesos**: Cambia los pesos a (H=0.4, N=0.4, Tf=0.2), recalcula el modelo y muestra la tabla actualizada.
4. **Genera gráfica 2**: Compara el índice original vs. el índice con pesos ajustados.
5. **Abre las ventanas a la vez**: las dos gráficas se muestran en paralelo.

## Solución de Problemas

### Matplotlib no muestra ventanas (Linux con Wayland)

Si las gráficas no aparecen en entornos Wayland, puedes cambiar el backend temporalmente:

```bash
export MPLBACKEND=TkAgg
python -m APE_1.main
```

### Error de módulo no encontrado

Asegúrate de estar ejecutando desde la ruta correcta. Si usas la Opción 1, debes estar en la raíz del proyecto (`APEs.py/`). Si usas la Opción 2, dentro de `APE_1/`.

### Error al activar entorno virtual en PowerShell

Si PowerShell bloquea la ejecución de scripts, ejecuta:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta activar nuevamente.
