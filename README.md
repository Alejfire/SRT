# Sistema de Matchmaking con Recursión y Programación Concurrente

## Descripción del Proyecto

Este programa simula un sistema básico de matchmaking para videojuegos, donde varios jugadores intentan entrar a una cola para ser emparejados en partidas.

El sistema utiliza programación concurrente mediante hilos (threads) para simular múltiples jugadores accediendo al sistema al mismo tiempo. Para evitar conflictos cuando varios hilos acceden a la misma cola, se utiliza un **semáforo** que controla el acceso al recurso compartido.

Además, el programa implementa un algoritmo recursivo para crear partidas automáticamente mientras existan al menos dos jugadores en la cola.

## Funcionamiento del Programa

1. Se crea una base de datos simulada de jugadores.
2. Cada jugador se ejecuta en un hilo independiente que intenta entrar a la cola de matchmaking.
3. Un semáforo controla el acceso a la cola para evitar conflictos entre hilos.
4. Cuando todos los jugadores han entrado a la cola, se ejecuta una **función recursiva** que:

   * Verifica si hay al menos dos jugadores disponibles.
   * Crea una partida entre ellos.
   * Guarda la partida en un historial.
   * Se llama nuevamente hasta que no queden suficientes jugadores.

## Tecnologías Utilizadas

* Python
* Programación concurrente con threading
* Semáforos para control de acceso
* Recursión
* Control de errores con excepciones
* Git para control de versiones

## Estructura del Proyecto

matchmaking.py
README.md
historial_partidas.txt

## Ejecución del Programa

Para ejecutar el programa:

1. Tener Python instalado.
2. Ejecutar el archivo principal:

python matchmaking.py

El programa mostrará en consola cómo los jugadores entran a la cola y cómo se crean las partidas.

## Video Demostrativo

Video mostrando la ejecución del programa: https://youtu.be/7owpRX2RLTg 
