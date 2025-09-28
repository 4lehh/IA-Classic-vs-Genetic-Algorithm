import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import questionary


def grafico_promedio_tiempo_agentes(datos: pd.DataFrame) -> None:
    nuevo_dataframe = datos.groupby("jugador")["tiempo"].mean()
    nuevo_dataframe.plot(kind="bar")

    plt.ylabel("Tiempo promedio (ms)")
    plt.xlabel("")
    plt.title("Tiempo promedio en milisegundos por agente")

    # Rotar labels
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def grafico_promedio_ticks_agentes(datos: pd.DataFrame) -> None:
    # Agrupar por jugador y calcular el promedio de tiempo
    nuevo_dataframe = datos.groupby("jugador")["ticks"].mean()
    nuevo_dataframe.plot(kind="bar")

    plt.ylabel("Ticks promedio")
    plt.xlabel("")
    plt.title("Ticks promedio por agente")

    # Rotar labels
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def grafico_exito_agentes(datos: pd.DataFrame) -> None:
    # Agrupar por jugador y calcular el promedio de tiempo
    nuevo_dataframe = datos.groupby("jugador")["llego"].mean()
    nuevo_dataframe.plot(kind="bar")

    plt.ylabel("Porcentaje de exito")
    plt.xlabel("")
    plt.title("Porcentaje de exito por agente")

    # Rotar labels
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def grafico_parametros_genetico_general(datos: pd.DataFrame) -> None:
    param_cols = ["alpha", "gamma", "betha", "omega"]

    # Filtramos solo los jugadores genéticos
    geneticos = datos[datos["jugador"] == "JugadorGenetico"].reset_index(drop=True)

    plt.figure(figsize=(10, 5))

    # Dibujamos cada parámetro como línea
    for param in param_cols:
        plt.plot(geneticos.index, geneticos[param], marker="o", label=param, alpha=0.7)

    plt.xlabel("Experimentos / Jugadores")
    plt.ylabel("Valor del parámetro")
    plt.title("Convergencia de parámetros en Jugadores Genéticos")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def grafico_tendencia_parametros(datos: pd.DataFrame) -> None:
    param_cols = ["alpha", "gamma", "betha", "omega"]
    geneticos = datos[datos["jugador"] == "JugadorGenetico"].reset_index(drop=True)

    plt.figure(figsize=(10, 5))

    for param in param_cols:
        y = geneticos[param].values
        x = geneticos.index.values

        # Graficamos los puntos
        plt.plot(x, y, "o", alpha=0.5, label=f"{param} datos")

        # Calculamos tendencia lineal
        coef = np.polyfit(x, y, 1)  # grado 1 = línea
        y_trend = np.polyval(coef, x)
        plt.plot(x, y_trend, "-", label=f"{param} tendencia")

    plt.xlabel("Experimentos / Jugadores")
    plt.ylabel("Valor del parámetro")
    plt.title("Tendencia de convergencia de parámetros (Jugadores Genéticos)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def elegir_grafico() -> None:
    # Mostrar el menú interactivo con las opciones de jugadores disponibles usando questionary.
    opciones = [
        "Gráfico de tiempo promedio por agente",
        "Gráfico de ticks promedio por agente",
        "Gráfico de porcentaje de éxito por agente",
        "Gráfico de parámetros del jugador genético (general)",
        "Gráfico de tendencia de parámetros del jugador genético",
    ]
    respuesta = questionary.select("Selecciona el tipo de jugador:", choices=opciones).ask()

    if respuesta is None:
        print("No se seleccionó ninguna opción.")
        return

    funciones = {
        "Gráfico de tiempo promedio por agente": grafico_promedio_tiempo_agentes,
        "Gráfico de ticks promedio por agente": grafico_promedio_ticks_agentes,
        "Gráfico de porcentaje de éxito por agente": grafico_exito_agentes,
        "Gráfico de parámetros del jugador genético (general)": grafico_parametros_genetico_general,
        "Gráfico de tendencia de parámetros del jugador genético": grafico_tendencia_parametros,
    }

    # Ejecutar la función correspondiente
    funcion_a_ejecutar = funciones.get(respuesta)
    if funcion_a_ejecutar:
        return funcion_a_ejecutar

    print("Opción no válida.")
    return


def elegir_filtros() -> tuple:
    # Preguntar por los filtros a aplicar
    opciones_dinamismo = ["0.01", "0.05", "0.1", "Todos"]
    opciones_probabilidad_muralla = ["0.1", "0.2", "0.3", "Todos"]
    opciones_tamanos = ["10", "25", "50", "100", "Todos"]

    tamanio = questionary.select(
        "Filtrar por tamaño (dejar vacío para no filtrar):", choices=opciones_tamanos
    ).ask()
    probabilidad_muralla = questionary.select(
        "Filtrar por probabilidad de muralla (dejar vacío para no filtrar):",
        choices=opciones_probabilidad_muralla,
    ).ask()
    dinamismo = questionary.select(
        "Selecciona el dinamismo de los muros:", choices=opciones_dinamismo
    ).ask()

    # Convertir a int o None
    dinamismo = float(dinamismo) if dinamismo and es_numero(dinamismo) else None
    probabilidad_muralla = (
        float(probabilidad_muralla)
        if probabilidad_muralla and es_numero(probabilidad_muralla)
        else None
    )
    tamanio = int(tamanio) if tamanio and tamanio.isdigit() else None

    return dinamismo, probabilidad_muralla, tamanio


def es_numero(valor: str) -> bool:
    try:
        float(valor)
        return True
    except ValueError:
        return False


def setear_parametros_csv(datos: pd.DataFrame) -> None:
    datos["prob_mover_murallas"] = datos["prob_mover_murallas"].astype(float)
    datos["prob_murallas"] = datos["prob_murallas"].astype(float)
    datos["filas"] = datos["filas"].astype(int)
    datos["columnas"] = datos["columnas"].astype(int)


def main():
    # Desde aquí se puede elegir qué gráfico generar y con qué filtros
    mi_funcion = elegir_grafico()
    dinamismo, probabilidad_muralla, tamanio = elegir_filtros()

    # Leemos los datos
    datos = pd.read_csv("./resultados/resultados.csv")

    # Setear los tipos de datos correctos
    setear_parametros_csv(datos)

    if dinamismo is not None:
        datos = datos[datos["prob_mover_murallas"] == dinamismo]

    if probabilidad_muralla is not None:
        datos = datos[datos["prob_murallas"] == probabilidad_muralla]

    if tamanio is not None:
        datos = datos[(datos["filas"] == tamanio) & (datos["columnas"] == tamanio)]

    mi_funcion(datos)


if __name__ == "__main__":
    main()
