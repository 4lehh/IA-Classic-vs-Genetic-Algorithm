# 🔍 Tarea 1: Algoritmos para resolución de laberintos dinámicos

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Implementación de algoritmos clásicos, algoritmos de aprendizaje por refuerzo y algoritmos genéticos para encontrar soluciones en entornos dinámicos.

<div align="center">
    <a href="./docs/Informe.pdf" target="_blank">
    <img src="https://img.shields.io/badge/📥_Descargar-PDF-red?style=for-the-badge" />
    </a>
</div>

</div>

## 👥 Integrantes del Equipo

| Nombres | Github | Matrícula |
|---------|--------|-----------|
|Antonio Jesus Benavides Puentes|[@AntoCreed777](https://github.com/AntoCreed777) | 2023455954 |
| Javier Alejandro Campos Contreras | [@4lehh](https://github.com/4lehh) | 2023432857 |

## 📋 Tabla de Contenidos
- [🚀 Inicio Rápido](#inicio-rapido)
- [🛠️ Tecnologías Utilizadas](#tecnologias-utilizadas)
- [📋 Requisitos Previos](#requisitos-previos)
- [⚙️ Instalación](#instalacion)
- [🔧 Configuración](#configuracion)
- [▶️ Ejecución](#ejecucion)
- [📊 Análisis de Resultados](#analisis-de-resultados)
- [🚀 Algoritmos Implementados](#algoritmos-implementados)
- [📈 Resultados y Análisis](#resultados-y-analisis)


## 🚀 Inicio Rápido

> [!IMPORTANT]
> **Prerequisitos**: Python 3.12

```bash
# Instalar pdm
pip install pdm

# Instalar las dependencias 
pdm install

# Ejecutar el código en Windows
pdm run python3 ./src/main.py -i
```

## 🛠️ Tecnologías Utilizadas

<div align="center">

### Herramientas de desarrollo y control de versiones
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=git,github,vscode&perline=5" />
</a>

### Lenguajes de programación
<a href="https://skillicons.dev">
  <img src="https://skillicons.dev/icons?i=python&perline=5" />
</a>

</div>

## 📋 Requisitos Previos

### Para Compilación y Ejecución
- **Python 3.12**
- **Sistema operativo:** Linux, macOS, o Windows

## ⚙️ Instalación

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/4lehh/IA-Classic-vs-Genetic-Algorithm
cd IA-Classic-vs-Genetic-Algorithm
```

### Dependencias

<details>
<summary>🪟 Windows</summary>

```bash
# En WSL (Ubuntu)
pip install pdm         # Usaremos pdm para manejar las dependencias
pdm install             # Instalará las dependencias necesarias
```

</details>
<details>
<summary>🐧 Linux (Ubuntu/Debian)</summary>

```bash
# Instalar Python y pip
sudo apt update
sudo apt install -y python3 python3-pip

# Instalar PDM
pip3 install pdm

# Ya dentro de la carpeta del proyecto
pdm install
```
</details>

## 🔧 Configuración

### Estructura del Proyecto

```
Proyecto_Semestral_Estructura_Datos/
├───resultados
│       resultados.csv
│
├───src                         # Código fuente (.py)
│   │   analizador.py
│   │   exceptions.py
│   │   laberinto.py
│   │   main.py
│   │   menu.py
│   │   simulacion.py
│   │   __init__.py
│   │
│   ├───jugador                 # Código de los agentes (.py)
│   │       jugador.py
│   │       jugador_a_estrella.py
│   │       jugador_genetico.py
│   │       jugador_greedy.py
│   │       jugador_q_learning.py
│   │       jugador_q_learning_adaptado.py
│   │       jugador_q_learning_estrella.py
│   │       jugador_random.py
│   │       __init__.py
│   │
│   └───models                  # Código de los modelos utilizados (.py)
│           casilla_laberinto.py
│           coordenada.py
│           movimientos.py
│           __init__.py
│   .pdm-python
│   experiments.sh              # Bash usado para la experimentación
│   pdm.lock                    
│   pyproject.toml
```

## ▶️ Ejecución

### Ejecutar Laberinto

```bash
# Ejecutar programa principal
pdm run python3 ./src/main.py -i

# Dentro habrá un menú selector donde eligirá el agente.
```

### Parámetros de Ejecución

- Seleccion de agentes con la flag `-a`
```bash
pdm run python3 ./src/main.py -i -a <Agente>
``` 
- **Agentes disponibles:**
  - JugadorRandom 
  - JugadorGreedy
  - JugadorAEstrella
  - JugadorQ-Learning
  - JugadorQ-LearningEstrella*
  - JugadorGenético

### Otros parámetros
- `-i`, `--interactivo`: Activa el modo interactivo.
- `-pg PROB`, `--prob-gen-murallas PROB`: Probabilidad de generar murallas (default: `0.2`),
- `-pm PROB`, `--prob-mover-murallas PROB`: Probabilidad de mover murallas (default: `0.01`).
- `-e`, `--experiments`: Activa el modo de experimentación.
- `--n-metas N`: Cantidad de metas a generar en el laberinto (default: `3`).

## 📊 Análisis de Resultados

> [!WARNING]
> **Ejecuta el modo experimentación:** El script de análisis requiere que exista un CSV llamado resultados.csv en resultados/. Asegúrate de tener los datos.

### Ejecutar Análisis Python

```bash
pdm run python3 ./src/analizador.py
```

### Gráficos Generados

El script de análisis genera automáticamente:

1. **Tiempo promedio en encontrar una solución:** Comparación de tiempos entre algoritmos.
2. **Ticks necesarios para encontrar una solución promedio:** Comparación de los ticks entre algoritmos.
3. **Porcentaje de éxito:** Analiza el desempeño de los agentes.
4. **Convergencia de parámetros en jugadores:** Estudia qué tanto convergen los valores (especialmente importante para el agente genético).

### Formato de Datos CSV

```bash
filas,columnas,prob_murallas,prob_mover_murallas,n_metas,tiempo,ticks,llego,jugador,alpha,gamma,betha,omega
```

## 🚀 Algoritmos Implementados

- **Random:** Algoritmo con movimientos pseudo-aleatorios.
- **Greedy:** Algoritmo que sigue una heurística simple.
- **LRTAStar (Learning Real-Time A Star):** Algoritmo que busca la mejor solución local, sumada a la función F tradicional de A*.
- **Q-Learning:** Algoritmo de aprendizaje por refuerzo.
- **Q-Learning + LRTAStar:** Algoritmo híbrido entre Q-Learning y LRTA*.
- **Genetico:** Algoritmo genetico implementado por el equipo basado en el hibrido Q-Learning + LRTA*.


## 📈 Resultados y Análisis

El proyecto permite comparar:

- **Tiempo de ejecución** entre diferentes algoritmos.
- **Tiempo de resolución** de laberintos dinámicos.
- **Eficiencia** para diferentes tipos de entornos dinámicos

---

<div align="center">

**Desarrollado con ❤️ para el curso de Inteligencia Artificial**

📚 **Universidad:** Universidad de Concepción  
🎓 **Curso:** Inteligencia Artificial  
📅 **Semestre:** 2025-2

</div>