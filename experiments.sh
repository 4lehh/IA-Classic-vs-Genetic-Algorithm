#!/bin/bash

# Número de repeticiones por configuración
N=50

# Jugadores a testear
jugadores=("JugadorAEstrella" "JugadorGenetico" "JugadorGreedy" "JugadorQlearning" "JugadorQlearningEstrella" "JugadorRandom")

# Tamaños de laberinto
tamanos=(10 25 50 100)

# Probabilidades de generar murallas
prob_gen=(0.1 0.2 0.3)

# Probabilidades de mover murallas
prob_move=(0.01 0.05 0.1)

# Carpeta
carpeta="./resultados/"

# Crear carpeta si no existe
mkdir -p "$carpeta"

# Recorremos jugadores, tamaños y probabilidades
OUTPUT="${carpeta}resultados.csv"

echo "filas,columnas,prob_murallas,prob_mover_murallas,n_metas,tiempo,ticks,llego,jugador,alpha,gamma,betha,omega" > "$OUTPUT"

for jugador in "${jugadores[@]}"; do
  for tam in "${tamanos[@]}"; do
    metas=$((tam/10)) # proporcional al tamaño
    for pg in "${prob_gen[@]}"; do
      for pm in "${prob_move[@]}"; do

        echo "Ejecutando $jugador tamaño ${tam}x${tam}, pg=$pg, pm=$pm, metas=$metas..."

        for ((i=1; i<=N; i++)); do
          pdm run python ./src/main.py -a $jugador -d $tam $tam --n-metas $metas -pg $pg -pm $pm -e >> "$OUTPUT"
        done

      done
    done
  done
done

echo "✅ Todos los experimentos terminados. Resultados guardados en $carpeta"
