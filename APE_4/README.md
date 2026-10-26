# APE 004 - Modelo SIR en Java y NetLogo

**Contenido**

- [1. Descripción del proyecto](#1-descripción-del-proyecto)
- [2. Tecnologías utilizadas](#2-tecnologías-utilizadas)
- [3. Instalación y configuración](#3-instalación-y-configuración)
- [4. Uso y ejecución del proyecto](#4-uso-y-ejecución-del-proyecto)
- [5. Estructura del proyecto](#5-estructura-del-proyecto)
- [6. Gestión de errores y registro de fallos](#6-gestión-de-errores-y-registro-de-fallos)

## 1. Descripción del proyecto

**Nombre:** APE 004 - Modelo SIR en Java y NetLogo.

**Propósito:** simular la propagación de una enfermedad en una población cerrada y permitir el análisis de la evolución de los estados epidemiológicos. El proyecto resuelve dos necesidades académicas: ejecutar un modelo SIR discreto y estocástico desde Java, con resultados exportables, y disponer de una representación basada en agentes en NetLogo para observar el comportamiento espacial de la población.

**Funcionalidades implementadas:**

- Simulación Java de una población de 100 individuos con estados susceptible, infectado y recuperado.
- Modelo Java con 5 infectados iniciales, contagio con probabilidad `beta = 0.30` y recuperación con probabilidad `gamma = 0.10` durante 100 pasos.
- Generación de `resultados_java.csv` con 101 registros de datos: tiempo 0 y pasos 1 a 100.
- Ejecución Java reproducible mediante una semilla numérica opcional.
- Validación de parámetros, transiciones de estado y conservación de la población.
- Modelo NetLogo con 100 agentes, 5 infectados iniciales, movimiento, contagio por proximidad y recuperación después de un número de ticks.
- Visualización NetLogo mediante monitores y tres gráficas: evolución de la población, personas infectadas y recuperación.
- Experimento NetLogo `simulacion-sir` para ejecución sin interfaz gráfica.

**Usuario objetivo:** estudiantes, docentes y personas con conocimientos básicos de Java o NetLogo que necesiten ejecutar, revisar o reproducir una práctica académica de simulación SIR.

### Cómo funciona el sistema

El proyecto contiene dos implementaciones independientes:

- **Java:** `Main` inicia el controlador con los parámetros fijados en el código. `ModeloSIR` representa a cada individuo mediante `Individuo` y aplica las transiciones `S -> I` e `I -> R` en pasos discretos. `ControladorSimulacion` recopila el historial, verifica que `S + I + R` se conserve y escribe el CSV. `VistaConsola` muestra el avance por la salida estándar.
- **NetLogo:** `setup` crea las tortugas, asigna estados y coloca 5 infectados. `go` mueve a los agentes, contagia susceptibles dentro del radio configurado, recupera infectados después de la duración indicada y actualiza monitores y gráficas. La simulación termina cuando no quedan infectados.

El modelo Java usa mezcla homogénea: cualquier susceptible puede contagiarse de cualquier infectado. El modelo NetLogo usa proximidad espacial y movimiento. Por ello, ambas implementaciones no producen necesariamente los mismos resultados y **el modelo NetLogo no carga el CSV generado por Java**.

No hay frontend web ni backend de servidor. La interfaz de Java es la consola; la interfaz de NetLogo es su aplicación de escritorio.

### Alcance y limitaciones

- Población cerrada, sin nacimientos, muertes ni reincorporación de recuperados.
- Los resultados son estocásticos y dependen de la semilla o de los números aleatorios.
- El modelo Java siempre ejecuta 100 pasos. El modelo NetLogo no tiene un límite fijo de ticks: se detiene cuando no quedan infectados, aunque el experimento headless tiene un límite de 201.
- No existe integración de lectura de CSV en NetLogo ni una comparación automática entre ambas implementaciones.
- No hay suite de pruebas automatizada.
- El proyecto implementa SIR, no M/M/1. Si la evaluación exige M/M/1, ese criterio está **Por definir** con el docente.

## 2. Tecnologías utilizadas

| Tecnología | Uso en el proyecto | Ubicación o componente |
|---|---|---|
| Java | Implementación del modelo SIR, controlador, vista de consola y exportación CSV. | `Main.java`, `model/`, `controller/`, `view/` |
| OpenJDK 25.0.4.1 | Versión de Java verificada para compilar y ejecutar. | `javac` y `java` del entorno |
| NetLogo 7.0.4 | Modelo basado en agentes, interfaz gráfica y experimento headless. | `modelo_sir_netlogo.nlogox`, `modelo_sir_netlogo_globals.nlogox` |
| CSV | Persistencia de los resultados de la simulación Java. | `resultados_java.csv` |
| `javac` / `java` | Compilación y ejecución directa, sin gestor de dependencias. | Comandos de la sección 3 y 4 |
| NetLogo Headless | Ejecución del experimento sin interfaz gráfica. | `/opt/netlogo/netlogo-headless.sh` |
| Git y GitHub | Control de versiones y repositorio remoto. | Repositorio `Practica3_MM1` |
| Markdown | Documentación del proyecto. | `README.md` |

**Lenguajes:** Java y NetLogo.

**Frameworks y librerías:** no se usan frameworks externos, Maven, Gradle, Spring, JUnit ni bibliotecas de terceros. Java utiliza únicamente la biblioteca estándar; NetLogo utiliza sus primitivas integradas.

**Frontend:** no hay frontend web. La salida Java es por consola y la visualización NetLogo se realiza en la interfaz de escritorio de NetLogo.

**Backend:** no hay servidor ni API HTTP. La lógica se ejecuta localmente en la máquina del usuario.

**Base de datos:** no se utiliza. El único almacenamiento es el archivo CSV generado por Java.

**Servicios externos o integraciones:** no hay integraciones en tiempo de ejecución. GitHub se usa únicamente como repositorio remoto de Git.

No se usa Python ni SimPy en este proyecto.

## 3. Instalación y configuración

### 3.1 Requisitos previos

| Requisito | Versión o condición verificada |
|---|---|
| Sistema operativo | Linux, entorno de verificación del proyecto |
| JDK | OpenJDK 25.0.4.1 |
| `javac` | Disponible en el `PATH` |
| NetLogo | 7.0.4 |
| NetLogo GUI | `/opt/netlogo/netlogo-gui.sh` |
| NetLogo Headless | `/opt/netlogo/netlogo-headless.sh` |

El proyecto Java no requiere dependencias externas, variables de entorno, base de datos ni servicios adicionales. NetLogo debe estar instalado; el repositorio no incluye su instalador.

Si NetLogo está instalado en otra ruta, reemplazar `/opt/netlogo` por la ruta correspondiente. El script de NetLogo utiliza `JAVA_HOME` si está definido; en caso contrario, usa `java` del `PATH`.

### 3.2 Obtener el proyecto

El remoto configurado del repositorio es:

```bash
git clone https://github.com/RichardC022/APEs.py.git
cd APEs.py/APE_4
```

Si ya se dispone de una copia local, no es necesario clonar y basta con situarse en la carpeta `APE_4`.

### 3.3 Verificar el entorno

```bash
java -version
javac -version
/opt/netlogo/netlogo-headless.sh --version
```

La última orden debe informar `NetLogo 7.0.4`. NetLogo puede mostrar advertencias de Java o de traducciones; son mensajes del entorno y no impiden ejecutar el modelo.

### 3.4 Compilar Java

Desde la carpeta `APE_4`:

```bash
javac -d build Main.java model/*.java controller/*.java view/*.java
```

El comando compila las clases y las coloca en `build/`. Esa carpeta se genera automáticamente y está incluida en `.gitignore`.

No hay que instalar dependencias del frontend ni del backend, configurar bases de datos ni crear archivos `.env`. El proyecto no incluye Docker ni archivos de configuración de servicios.

## 4. Uso y ejecución del proyecto

### 4.1 Ejecutar la simulación Java

Sin semilla explícita:

```bash
java -cp build Main
```

La semilla se obtiene de `System.nanoTime()` y se imprime en la consola.

Con una semilla fija:

```bash
java -cp build Main 123
```

La semilla permite reproducir una ejecución. El programa escribe `resultados_java.csv` en el directorio de trabajo actual y muestra su ruta absoluta.

Ejemplo de salida con semilla `123`:

```text
Semilla utilizada: 123
=================================================
   INICIANDO SIMULACIÓN MODELO EPIDEMIOLÓGICO SIR
=================================================
Paso   0: S =  95 | I =   5 | R =   0
...
Paso 100: S =   0 | I =   0 | R = 100
=================================================
Simulación finalizada.
Archivo CSV generado: /ruta/APE_4/resultados_java.csv
=================================================
```

El CSV generado tiene este formato:

```csv
tiempo,susceptibles,infectados,recuperados
0,95,5,0
1,14,86,0
2,0,88,12
...
100,0,0,100
```

Incluye 101 filas de datos, sin contar el encabezado. La escritura se realiza en UTF-8.

**Parámetros fijados en `Main.java`:**

| Parámetro | Valor |
|---|---:|
| Población total | 100 |
| Infectados iniciales | 5 |
| `beta` (infección) | 0.30 |
| `gamma` (recuperación) | 0.10 |
| Pasos de simulación | 100 |

Para modificar estos valores es necesario editar `Main.java` y recompilar. El modelo Java usa los estados existentes al inicio de cada paso; las infecciones y recuperaciones calculadas se aplican al final del paso.

**Códigos de salida de Java:**

| Código | Significado |
|---:|---|
| `0` | Simulación completada y CSV generado correctamente. |
| `1` | Error de conservación de población o imposibilidad de escribir el CSV. |
| `2` | Argumentos inválidos: más de un argumento o semilla no numérica. |

### 4.2 Ejecutar NetLogo con interfaz gráfica

Desde `APE_4`:

```bash
/opt/netlogo/netlogo-gui.sh "$(pwd)/modelo_sir_netlogo.nlogox"
```

Dentro de NetLogo:

1. Abrir la pestaña **Interface**.
2. Pulsar **Setup**. Se crean 100 personas: 95 susceptibles, 5 infectadas y 0 recuperadas.
3. Pulsar **Go**. La simulación avanza hasta que no quedan infectados.
4. Observar los monitores y las gráficas.

El botón **Go** está deshabilitado hasta que se ejecuta **Setup**.

**Parámetros del modelo NetLogo con sliders:**

| Control | Valor inicial | Rango | Efecto |
|---|---:|---:|---|
| `Población` | 100 | 10 a 500 | Cantidad de tortugas creadas. |
| `Radio de contagio` | 3 | 0 a 10 | Distancia para buscar susceptibles cercanos. |
| `Probabilidad de contagio (%)` | 30 | 0 a 100 | Probabilidad de contagio por contacto. |
| `Duración de la infección` | 10 | 1 a 50 | Ticks necesarios para recuperarse. |

El modelo incluye:

- Vista del mundo con agentes verdes (susceptibles), rojos (infectados) y azules (recuperados).
- Monitores de susceptibles, infectados y recuperados.
- Gráfica **Evolucion de la poblacion** con las tres series.
- Gráfica **Personas infectadas**.
- Gráfica **Recuperacion**.

El modelo NetLogo es independiente del CSV de Java: no importa `resultados_java.csv` ni compara sus resultados con la simulación Java.

**Alternativa sin sliders:** si al abrir el modelo aparece el error `Nothing named POBLACION has been defined`, usar:

```bash
/opt/netlogo/netlogo-gui.sh "$(pwd)/modelo_sir_netlogo_globals.nlogox"
```

Ese archivo define `poblacion`, `radio-contagio`, `prob-contagio` y `duracion` directamente en `setup`, por lo que no depende de la carga de sliders. Los valores se modifican en el código del archivo.

### 4.3 Ejecutar NetLogo sin interfaz gráfica

El modelo incluye el experimento `simulacion-sir`, con 5 repeticiones, límite de 201 ticks y métricas por paso:

```bash
/opt/netlogo/netlogo-headless.sh --headless \
  --model "$(pwd)/modelo_sir_netlogo.nlogox" \
  --experiment simulacion-sir \
  --threads 1 \
  --table /tmp/resultados_netlogo.csv
```

El archivo `/tmp/resultados_netlogo.csv` contiene las métricas `ticks`, `total-susceptibles`, `total-infectados`, `total-recuperados` y `count turtles`. También puede enviarse la tabla a la salida estándar con `--table -`.

NetLogo 7 usa el formato `.nlogox`. Renombrar el archivo a `.nlogo` no funciona en esta versión.

### 4.4 Pruebas y verificación manual

No hay una suite de pruebas automatizada ni un comando de pruebas configurado. Las verificaciones disponibles son manuales:

**Reproducibilidad de Java:**

```bash
java -cp build Main 123
sha256sum resultados_java.csv
java -cp build Main 123
sha256sum resultados_java.csv
```

Las dos ejecuciones deben producir el mismo hash y, por tanto, el mismo contenido CSV.

**Validación de argumentos:**

```bash
java -cp build Main 1 2
java -cp build Main abc
```

Ambos comandos deben terminar con código `2`.

**Verificación de NetLogo:**

```bash
/opt/netlogo/netlogo-headless.sh --headless \
  --model "$(pwd)/modelo_sir_netlogo.nlogox" \
  --experiment simulacion-sir \
  --threads 1 \
  --table /tmp/resultados_netlogo.csv
```

La ejecución debe terminar con código `0`. En la prueba realizada, las cinco corridas comenzaron con 95 susceptibles, 5 infectados y 0 recuperados, y finalizaron sin infectados.

No hay comandos de desarrollo, pruebas o producción adicionales, ni una dirección local de acceso web, porque el proyecto no expone un servidor HTTP ni una API.

## 5. Estructura del proyecto

```text
APE_4/
├── Main.java
├── model/
│   ├── Estado.java
│   ├── Individuo.java
│   ├── ModeloSIR.java
│   └── Resultado.java
├── controller/
│   └── ControladorSimulacion.java
├── view/
│   └── VistaConsola.java
├── modelo_sir_netlogo.nlogox
├── modelo_sir_netlogo_globals.nlogox
├── README.md
└── .gitignore
```

Los archivos `build/` y `resultados_java.csv` se generan durante la compilación y ejecución. Ambos están incluidos en `.gitignore` y no forman parte del código fuente versionado.

| Archivo o carpeta | Responsabilidad |
|---|---|
| `Main.java` | Punto de entrada Java. Define población, infectados iniciales, probabilidades, pasos y semilla; valida los argumentos y controla los códigos de salida. |
| `model/Estado.java` | Enumera los estados `SUSCEPTIBLE`, `INFECTADO` y `RECUPERADO`. |
| `model/Individuo.java` | Representa un agente con identificador y estado; restringe las transiciones a `S -> I` e `I -> R`. |
| `model/ModeloSIR.java` | Contiene la lógica del modelo, la generación aleatoria con semilla, el avance de pasos y el conteo de estados. |
| `model/Resultado.java` | Almacena un registro inmutable de tiempo, susceptibles, infectados y recuperados; genera una línea CSV. |
| `controller/ControladorSimulacion.java` | Coordina la simulación, conserva el historial, verifica la conservación de la población y escribe el CSV. |
| `view/VistaConsola.java` | Presenta el inicio, cada paso, el resultado final y los errores en consola. |
| `modelo_sir_netlogo.nlogox` | Modelo NetLogo con sliders, monitores, gráficas y el experimento `simulacion-sir`. |
| `modelo_sir_netlogo_globals.nlogox` | Variante del modelo NetLogo que fija los parámetros en el código y no depende de sliders. |
| `.gitignore` | Excluye clases compiladas, `build/` y `resultados_java.csv` del control de versiones. |
| `README.md` | Documentación del proyecto. |

La relación principal de Java es: `Main -> ControladorSimulacion -> ModeloSIR -> Individuo/Resultado`, con `VistaConsola` para la salida y el CSV como persistencia. NetLogo es una implementación separada: su procedimiento `setup` crea los agentes y `go` ejecuta movimiento, contagio, recuperación y actualización de gráficas.

## 6. Gestión de errores y registro de fallos

No existe un framework de logging, un archivo de logs ni un sistema centralizado de errores. Java informa mediante `System.out` y `System.err`; NetLogo muestra los errores en su interfaz o en la salida de la ejecución headless.

### 6.1 Validaciones y manejo de errores en Java

| Componente | Validación o manejo | Resultado |
|---|---|---|
| `Main` | Más de un argumento. | Mensaje de uso y salida con código `2`. |
| `Main` | Semilla no numérica. | Mensaje de error y salida con código `2`. |
| `ModeloSIR` | Población total mayor que cero. | `IllegalArgumentException`. |
| `ModeloSIR` | Infectados iniciales entre 0 y la población. | `IllegalArgumentException`. |
| `ModeloSIR` | `beta` y `gamma` finitos y entre 0 y 1. | `IllegalArgumentException`. |
| `Individuo` | ID no negativo y estado no nulo. | `IllegalArgumentException`. |
| `Individuo` | Solo permite `S -> I` e `I -> R`. | `IllegalStateException` ante una transición inválida. |
| `Resultado` | Tiempo y contadores no negativos. | `IllegalArgumentException`. |
| `ControladorSimulacion` | `S + I + R` debe ser igual a la población total. | Muestra el error y devuelve `false`; `Main` termina con código `1`. |
| `ControladorSimulacion` | Error de escritura del CSV. | Muestra el error y devuelve `false`; `Main` termina con código `1`. |

Los errores de escritura incluyen la ruta absoluta del archivo y el mensaje de la excepción `IOException`. No se registran en un archivo de log.

### 6.2 Comportamiento ante errores en NetLogo

- `go` se detiene cuando no quedan tortugas infectadas.
- No hay validación personalizada de sliders ni un manejador centralizado de errores.
- No se escribe un log desde NetLogo.
- El experimento headless informa los errores en la salida estándar; el código de salida permite detectar fallos. En la verificación realizada, la ejecución terminó con código `0`.
- Los mensajes `unable to find translation for...` de NetLogo en español son advertencias de localización y no errores del modelo.

### 6.3 Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `Nothing named POBLACION has been defined` | El modelo abierto no define `poblacion`; suele ocurrir al pegar solo el código sin sliders o al usar una ventana antigua. | Abrir `modelo_sir_netlogo_globals.nlogox` o usar el archivo con sliders sin pegar el código en un modelo nuevo. |
| NetLogo no abre el archivo | Se está usando la extensión `.nlogo` con NetLogo 7. | Usar el archivo `.nlogox` original. |
| `Go` no responde | No se ha ejecutado `Setup`; el botón está deshabilitado hasta que haya ticks. | Pulsar primero **Setup**. |
| Las gráficas están vacías | La simulación no ha comenzado. | Ejecutar **Setup** y después **Go**. |
| No se crea `resultados_java.csv` | El directorio de trabajo no tiene permisos de escritura. | Ejecutar desde un directorio escribible; el programa mostrará la ruta y terminará con código `1`. |
| `javac: command not found` | El JDK no está instalado o no está en el `PATH`. | Instalar un JDK compatible y verificar con `javac -version`. |
| No se encuentra NetLogo | La ruta `/opt/netlogo` no corresponde a la instalación. | Ajustar la ruta de `netlogo-gui.sh` o `netlogo-headless.sh`. |
| Error relacionado con la forma `person` | Se modificó o reemplazó el modelo y se perdió la definición de la forma. | Usar los archivos incluidos, que ya contienen la definición de `person`. |

### 6.4 Diagnóstico recomendado

1. Verificar las versiones con `java -version`, `javac -version` y `/opt/netlogo/netlogo-headless.sh --version`.
2. Compilar de nuevo con el comando de la sección 3 y revisar los mensajes de `javac`.
3. Ejecutar Java desde una carpeta con permisos de escritura y comprobar la ruta impresa para el CSV.
4. En NetLogo, confirmar que el título de la ventana corresponde al archivo `.nlogox` correcto, ejecutar **Setup** antes de **Go** y revisar la pestaña **Interface**.
5. Para aislar problemas de sliders, usar `modelo_sir_netlogo_globals.nlogox`.
6. Ejecutar el experimento headless para comprobar si el fallo está en la interfaz gráfica o en la lógica del modelo.
