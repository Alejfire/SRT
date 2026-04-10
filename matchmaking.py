"""
Proyecto Final - Sistema de Matchmaking en Tiempo Real

Descripción:
Este sistema simula un entorno de matchmaking competitivo donde múltiples
jugadores acceden concurrentemente a una cola para ser emparejados.

Características:
- Uso de hilos para concurrencia
- Implementación de semáforos para sincronización
- Emparejamiento basado en MMR
- Registro de partidas en archivo
"""

import threading
import time
from collections import deque
from random import uniform

users_db = {
    "Alejfire": {"mmr": 1200},
    "AliceTowers": {"mmr": 1150},
    "Minecrafter100": {"mmr": 1100},
    "ShadowSn1per": {"mmr": 1180},
    "NovaStrike": {"mmr": 1120},
    "PixelWarrior": {"mmr": 1090}
}

matchmaking_queue = deque()
match_history = []

queue_semaphore = threading.Semaphore(1)


def join_matchmaking(player):
    """Agrega un jugador a la cola de matchmaking de forma segura"""
    print(f"{player} está intentando entrar a la cola...")
    time.sleep(uniform(0.1, 0.5))

    queue_semaphore.acquire()
    try:
        print(f"🟢 {player} accedió a la sección crítica")

        matchmaking_queue.append(player)
        print(f"{player} entró a la cola. Total en cola: {len(matchmaking_queue)}")

        time.sleep(1)

        print(f"🔴 {player} sale de la sección crítica")
    finally:
        queue_semaphore.release()


def match_players():
    """Empareja jugadores basándose en su MMR"""
    queue_semaphore.acquire()
    try:
        if len(matchmaking_queue) < 2:
            return None

        sorted_players = sorted(list(matchmaking_queue), key=lambda p: users_db[p]["mmr"])

        p1 = sorted_players[0]
        p2 = sorted_players[1]

        matchmaking_queue.remove(p1)
        matchmaking_queue.remove(p2)

        match_id = len(match_history) + 1
        match = {"id": match_id, "players": [p1, p2]}

        match_history.append(match)
        save_match(match)

        print(f"\n🎮 Partida creada: {p1} vs {p2}\n")

        return match
    finally:
        queue_semaphore.release()


def save_match(match):
    """Guarda el historial de partidas en un archivo"""
    with open("historial_partidas.txt", "a") as f:
        f.write(f"Partida {match['id']}: {match['players'][0]} vs {match['players'][1]}\n")


def simulate_player(player):
    """Simula un jugador entrando al sistema"""
    join_matchmaking(player)


def run_matchmaking():
    """Ejecuta el sistema completo"""
    open("historial_partidas.txt", "w").close()

    threads = []

    for player in users_db.keys():
        t = threading.Thread(target=simulate_player, args=(player,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nCreando partidas...\n")

    while len(matchmaking_queue) >= 2:
        match_players()
        time.sleep(1)

    print("\nHistorial final:")
    print(match_history)


if __name__ == "__main__":
    run_matchmaking()